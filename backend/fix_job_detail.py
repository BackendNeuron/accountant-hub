with open('app/services/job_service.py', 'r') as f:
    content = f.read()

old_get = 'async def get_job_detail(self, job_id: int) -> dict:'
new_get = 'async def get_job_detail(self, job_id: int, current_user = None) -> dict:'
content = content.replace(old_get, new_get)

old_return = 'return {"job": job, "current_user_bid": None}'
new_return = '''current_user_bid = None
        if current_user and current_user.role == "accountant":
            bid_result = await self.db.execute(
                select(Bid).where(Bid.job_id == job_id, Bid.accountant_id == current_user.id)
            )
            bid = bid_result.scalar_one_or_none()
            if bid:
                current_user_bid = {
                    "id": bid.id,
                    "price": str(bid.price),
                    "status": bid.status,
                    "submitted_at": str(bid.created_at),
                }
        return {"job": job, "current_user_bid": current_user_bid}'''
content = content.replace(old_return, new_return)

with open('app/services/job_service.py', 'w') as f:
    f.write(content)

print('Done')
