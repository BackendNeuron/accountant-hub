from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from app.models.job import Job
from app.models.user import User
from app.models.accountant_profile import AccountantProfile
from app.models.accountant_certification import AccountantCertification
from app.models.certification import Certification
from app.models.accountant_software_skill import AccountantSoftwareSkill
from app.models.software_skill import SoftwareSkill


class MatchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_match(self, job_id: int, accountant: User) -> dict:
        result = await self.db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if not job or accountant.role != 'accountant':
            return {'score': 0, 'matched': [], 'missing': [], 'warnings': []}

        profile_result = await self.db.execute(
            select(AccountantProfile).where(AccountantProfile.user_id == accountant.id)
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            return {
                'score': 0,
                'matched': [],
                'missing': ['Complete your profile to see match scores'],
                'warnings': ['Profile incomplete - complete it to increase your chances'],
            }

        matched = []
        missing = []
        warnings = []
        total_checks = 0

        # Get accountant certifications
        cert_result = await self.db.execute(
            select(AccountantCertification).where(
                AccountantCertification.accountant_profile_id == profile.id
            )
        )
        acct_certs = cert_result.scalars().all()
        
        accountant_cert_names = []
        for ac in acct_certs:
            if ac.certification_id:
                cert_res = await self.db.execute(
                    select(Certification).where(Certification.id == ac.certification_id)
                )
                cert = cert_res.scalar_one_or_none()
                cert_name = cert.name if cert else None
            else:
                cert_name = ac.custom_certification_name
            
            if cert_name:
                if ac.expiry_date and ac.expiry_date < date.today():
                    warnings.append(f"Certification '{cert_name}' is expired")
                    continue
                if ac.expiry_date and (ac.expiry_date - date.today()).days <= 30:
                    warnings.append(f"Certification '{cert_name}' expires soon")
                accountant_cert_names.append(cert_name)

        # Check required certifications
        if job.required_certifications and len(job.required_certifications) > 0:
            total_checks += len(job.required_certifications)
            for req_cert in job.required_certifications:
                if req_cert in accountant_cert_names:
                    matched.append(f'Certification: {req_cert}')
                else:
                    missing.append(f'Certification: {req_cert}')

        # Get accountant software skills
        sw_result = await self.db.execute(
            select(AccountantSoftwareSkill).where(
                AccountantSoftwareSkill.accountant_profile_id == profile.id
            )
        )
        acct_sw = sw_result.scalars().all()
        
        accountant_software_names = []
        for ass in acct_sw:
            sw_res = await self.db.execute(
                select(SoftwareSkill).where(SoftwareSkill.id == ass.software_skill_id)
            )
            sw = sw_res.scalar_one_or_none()
            if sw:
                accountant_software_names.append(sw.name)

        # Check required software
        if job.required_software and len(job.required_software) > 0:
            total_checks += len(job.required_software)
            for req_sw in job.required_software:
                if req_sw in accountant_software_names:
                    matched.append(f'Software: {req_sw}')
                else:
                    missing.append(f'Software: {req_sw}')

        # Check jurisdiction
        if job.jurisdiction:
            total_checks += 1
            if profile.jurisdictions_served and job.jurisdiction in profile.jurisdictions_served:
                matched.append(f'Jurisdiction: {job.jurisdiction}')
            else:
                missing.append(f'Jurisdiction: {job.jurisdiction}')
                warnings.append(f'This job requires {job.jurisdiction} jurisdiction - not in your profile')

        # Check accounting standard
        if job.accounting_standard:
            total_checks += 1
            if profile.accounting_standards and job.accounting_standard in profile.accounting_standards:
                matched.append(f'Standard: {job.accounting_standard}')
            else:
                missing.append(f'Standard: {job.accounting_standard}')

        # Check experience
        if job.minimum_experience_years:
            total_checks += 1
            if profile.years_of_experience and profile.years_of_experience >= job.minimum_experience_years:
                matched.append(f'Experience: {profile.years_of_experience} years (requires {job.minimum_experience_years})')
            else:
                missing.append(f'Experience: Requires {job.minimum_experience_years}+ years')

        score = round((len(matched) / total_checks * 100)) if total_checks > 0 else 100

        return {
            'score': score,
            'matched': matched,
            'missing': missing,
            'warnings': warnings,
        }
