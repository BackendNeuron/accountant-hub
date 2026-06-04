"""
Accountant Hub - Frontend Setup Phase I
Core: Theme, i18n, Auth, Routing, Layout, Component Library
Run: python setup_frontend_phase1.py
"""
import os
import py_compile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "src")
ERRORS = []
CREATED = []
MODIFIED = []

def write_file(rel_path, content):
    filepath = os.path.join(FRONTEND_DIR, rel_path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existed = os.path.exists(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    if existed:
        MODIFIED.append(filepath)
    else:
        CREATED.append(filepath)
    print(f"  {'🔧' if existed else '✅'} {'Updated' if existed else 'Created'}: {rel_path}")

def verify_jsx(filepath):
    """Basic syntax check for JSX files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"  ✅ Verified: {os.path.relpath(filepath, FRONTEND_DIR)}")
        return True
    except SyntaxError as e:
        print(f"  ❌ SYNTAX ERROR in {os.path.relpath(filepath, FRONTEND_DIR)}: {e}")
        ERRORS.append((filepath, str(e)))
        return False

def setup_theme_and_styles():
    """Step 1: Global styles, theme CSS, animations"""
    print("\n" + "="*60)
    print("STEP 1: Theme System & Global Styles")
    print("="*60)

    write_file("styles/theme.css", THEME_CSS)
    write_file("styles/global.css", GLOBAL_CSS)
    write_file("styles/animations.css", ANIMATIONS_CSS)

def setup_i18n():
    """Step 2: i18n setup + EN/AR translations"""
    print("\n" + "="*60)
    print("STEP 2: Internationalization (EN/AR)")
    print("="*60)

    write_file("i18n/index.js", I18N_INDEX)
    write_file("i18n/en.json", EN_JSON)
    write_file("i18n/ar.json", AR_JSON)

def setup_hooks():
    """Step 3: Custom hooks"""
    print("\n" + "="*60)
    print("STEP 3: Custom Hooks")
    print("="*60)

    write_file("hooks/useAuth.js", USE_AUTH)
    write_file("hooks/useTheme.js", USE_THEME)
    write_file("hooks/useLanguage.js", USE_LANGUAGE)
    write_file("hooks/useDebounce.js", USE_DEBOUNCE)

def setup_context():
    """Step 4: Auth + Toast Context"""
    print("\n" + "="*60)
    print("STEP 4: Context Providers")
    print("="*60)

    write_file("context/AuthContext.jsx", AUTH_CONTEXT)
    write_file("context/ToastContext.jsx", TOAST_CONTEXT)

def setup_services():
    """Step 5: API services"""
    print("\n" + "="*60)
    print("STEP 5: API Service Layer")
    print("="*60)

    write_file("services/api.js", API_SERVICE)
    write_file("services/authService.js", AUTH_SERVICE)
    write_file("services/jobService.js", JOB_SERVICE)
    write_file("services/bidService.js", BID_SERVICE)
    write_file("services/profileService.js", PROFILE_SERVICE)
    write_file("services/adminService.js", ADMIN_SERVICE)

def setup_utils():
    """Step 6: Utility functions"""
    print("\n" + "="*60)
    print("STEP 6: Utilities")
    print("="*60)

    write_file("utils/formatDate.js", FORMAT_DATE)
    write_file("utils/formatCurrency.js", FORMAT_CURRENCY)
    write_file("utils/constants.js", CONSTANTS)

def setup_ui_components():
    """Step 7: Reusable UI components"""
    print("\n" + "="*60)
    print("STEP 7: UI Component Library")
    print("="*60)

    components = [
        ("Button.jsx", BUTTON_JSX),
        ("Input.jsx", INPUT_JSX),
        ("Select.jsx", SELECT_JSX),
        ("Textarea.jsx", TEXTAREA_JSX),
        ("Badge.jsx", BADGE_JSX),
        ("Card.jsx", CARD_JSX),
        ("Modal.jsx", MODAL_JSX),
        ("Skeleton.jsx", SKELETON_JSX),
        ("Pagination.jsx", PAGINATION_JSX),
        ("SearchBar.jsx", SEARCHBAR_JSX),
        ("EmptyState.jsx", EMPTYSTATE_JSX),
        ("Toast.jsx", TOAST_JSX),
        ("Spinner.jsx", SPINNER_JSX),
        ("MultiSelect.jsx", MULTISELECT_JSX),
        ("DisclaimerBanner.jsx", DISCLAIMER_BANNER_JSX),
    ]
    for filename, content in components:
        write_file(f"components/ui/{filename}", content)

def setup_layout():
    """Step 8: Layout components"""
    print("\n" + "="*60)
    print("STEP 8: Layout (Navbar, Footer, Sidebar)")
    print("="*60)

    write_file("components/layout/Navbar.jsx", NAVBAR_JSX)
    write_file("components/layout/Footer.jsx", FOOTER_JSX)
    write_file("components/layout/Sidebar.jsx", SIDEBAR_JSX)
    write_file("components/layout/Layout.jsx", LAYOUT_JSX)
    write_file("components/layout/ProtectedRoute.jsx", PROTECTED_ROUTE_JSX)

def setup_app_entry():
    """Step 9: App.jsx, main.jsx, index.html update"""
    print("\n" + "="*60)
    print("STEP 9: App Entry Point & Routing")
    print("="*60)

    write_file("App.jsx", APP_JSX)
    write_file("main.jsx", MAIN_JSX)

def print_summary():
    print("\n" + "="*60)
    print("FRONTEND PHASE I COMPLETE")
    print("="*60)
    if CREATED:
        print(f"\n📁 {len(CREATED)} files created")
    if MODIFIED:
        print(f"\n🔧 {len(MODIFIED)} files updated")
    if ERRORS:
        print(f"\n❌ {len(ERRORS)} syntax errors")
    else:
        print(f"\n✅ All files created successfully")
    print(f"\nNext: python setup_frontend_phase2.py (all pages)")

# ============================================================
# FILE CONTENTS
# ============================================================

THEME_CSS = '''
/* ============================================
   Accountant Hub — Theme Tokens
   ============================================ */

/* Light Theme (default) */
[data-theme="light"] {
  --color-bg-page: #F5F5F0;
  --color-bg-surface: #FFFFFF;
  --color-bg-surface-2: #F9FAFB;
  --color-bg-hover: #F3F4F6;
  --color-border: #E5E7EB;
  --color-border-strong: #D1D5DB;
  --color-text-primary: #111111;
  --color-text-secondary: #4B5563;
  --color-text-muted: #9CA3AF;
  --color-text-placeholder: #9CA3AF;
  --color-primary: #019A51;
  --color-primary-dark: #017A41;
  --color-primary-light: #E6F5ED;
  --color-primary-text: #014D29;
  --color-status-open-bg: #E6F5ED;
  --color-status-open-text: #019A51;
  --color-status-closed-bg: #FEE2E2;
  --color-status-closed-text: #991B1B;
  --color-danger: #EF4444;
  --color-danger-light: #FEE2E2;
  --color-warning: #F59E0B;
  --color-warning-light: #FEF3C7;
  --color-shadow: rgba(0,0,0,0.06);
  --color-backdrop: rgba(0,0,0,0.5);
  --color-skeleton: #E5E7EB;
  --color-skeleton-shine: #F3F4F6;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --radius-xl: 12px;
  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
}

/* Dark Theme */
[data-theme="dark"] {
  --color-bg-page: #000000;
  --color-bg-surface: #0D0D0D;
  --color-bg-surface-2: #111111;
  --color-bg-hover: #1A1A1A;
  --color-border: #1A1A1A;
  --color-border-strong: #2A2A2A;
  --color-text-primary: #F9FAFB;
  --color-text-secondary: #9CA3AF;
  --color-text-muted: #6B7280;
  --color-text-placeholder: #4B5563;
  --color-primary: #019A51;
  --color-primary-dark: #017A41;
  --color-primary-light: #0D2318;
  --color-primary-text: #4ADE80;
  --color-status-open-bg: #0D2318;
  --color-status-open-text: #4ADE80;
  --color-status-closed-bg: #200A0A;
  --color-status-closed-text: #F87171;
  --color-danger: #F87171;
  --color-danger-light: #200A0A;
  --color-warning: #FCD34D;
  --color-warning-light: #1A1400;
  --color-shadow: rgba(0,0,0,0.4);
  --color-backdrop: rgba(0,0,0,0.7);
  --color-skeleton: #1A1A1A;
  --color-skeleton-shine: #2A2A2A;
}
'''

GLOBAL_CSS = '''
/* ============================================
   Accountant Hub — Global Styles
   ============================================ */

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600&display=swap');

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text-secondary);
  background-color: var(--color-bg-page);
  transition: background-color 0.3s ease, color 0.3s ease;
  min-height: 100vh;
}

/* Arabic font */
[lang="ar"] body,
[dir="rtl"] body {
  font-family: 'Cairo', sans-serif;
}

/* RTL overrides */
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .ml-auto { margin-left: 0; margin-right: auto; }
[dir="rtl"] .mr-auto { margin-right: 0; margin-left: auto; }

h1, h2, h3, h4 {
  color: var(--color-text-primary);
  font-weight: 600;
  line-height: 1.3;
}

h1 {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
}

h2 {
  font-family: 'DM Sans', sans-serif;
  font-size: 20px;
}

h3 {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
}

[lang="ar"] h1,
[dir="rtl"] h1 {
  font-family: 'Cairo', sans-serif;
}

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: var(--color-primary-dark);
}

img {
  max-width: 100%;
  height: auto;
}

button {
  cursor: pointer;
  font-family: inherit;
  border: none;
  outline: none;
}

input, textarea, select {
  font-family: inherit;
  font-size: inherit;
}

/* Utility classes */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--color-border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }

/* Selection */
::selection {
  background: var(--color-primary-light);
  color: var(--color-primary-text);
}
'''

ANIMATIONS_CSS = '''
/* ============================================
   Accountant Hub — Animations
   ============================================ */

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

@keyframes slideInRight {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

@keyframes slideOutRight {
  from { transform: translateX(0); }
  to { transform: translateX(100%); }
}

@keyframes slideInUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-fade-in {
  animation: fadeIn 0.25s ease forwards;
}

.animate-slide-right {
  animation: slideInRight 0.3s ease forwards;
}

.animate-slide-up {
  animation: slideInUp 0.3s ease forwards;
}

.animate-scale-in {
  animation: scaleIn 0.2s ease forwards;
}

.animate-spin {
  animation: spin 0.8s linear infinite;
}

.animate-pulse {
  animation: pulse 2s ease-in-out infinite;
}
'''

I18N_INDEX = '''
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './en.json';
import ar from './ar.json';

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    ar: { translation: ar },
  },
  lng: localStorage.getItem('ah_lang') || 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
'''

EN_JSON = '''
{
  "nav": {
    "browseJobs": "Browse Jobs",
    "dashboard": "Dashboard",
    "myBids": "My Bids",
    "myJobs": "My Jobs",
    "profile": "Profile",
    "login": "Login",
    "register": "Register",
    "logout": "Logout",
    "postJob": "Post a Job",
    "admin": "Admin Panel"
  },
  "hero": {
    "title": "Find Accounting Jobs",
    "subtitle": "Browse hundreds of accounting & finance opportunities from verified businesses"
  },
  "jobCard": {
    "budget": "Budget",
    "deadline": "Deadline",
    "bids": "bids",
    "posted": "Posted",
    "open": "Open",
    "closed": "Closed",
    "viewDetails": "View Details"
  },
  "filters": {
    "title": "Filters",
    "search": "Search jobs...",
    "category": "Category",
    "budgetRange": "Budget Range",
    "standard": "Accounting Standard",
    "jurisdiction": "Jurisdiction",
    "status": "Status",
    "all": "All",
    "openOnly": "Open Only",
    "closedOnly": "Closed Only",
    "sortBy": "Sort by",
    "newest": "Newest",
    "highestBudget": "Highest Budget",
    "mostBids": "Most Bids",
    "clearAll": "Clear All Filters"
  },
  "jobDetail": {
    "budget": "Budget",
    "deadline": "Deadline",
    "delivery": "Expected Delivery",
    "bidsReceived": "Bids Received",
    "requiredSkills": "Required Skills",
    "certifications": "Certifications",
    "software": "Software",
    "standard": "Standard",
    "jurisdiction": "Jurisdiction",
    "attachments": "Attachments",
    "noAttachments": "No attachments",
    "submitBid": "Submit Bid",
    "alreadyBid": "You have submitted a bid",
    "jobClosed": "This job is closed",
    "ndaRequired": "NDA Required",
    "acceptNda": "Accept NDA to View Details",
    "matchScore": "Match Score"
  },
  "bidForm": {
    "title": "Submit Your Proposal",
    "price": "Proposed Price",
    "pricingModel": "Pricing Model",
    "fixed": "Fixed Price",
    "hourly": "Hourly",
    "retainer": "Retainer",
    "deliveryTime": "Estimated Delivery Time",
    "estimatedHours": "Estimated Hours",
    "coverLetter": "Cover Letter / Proposal",
    "experience": "Relevant Experience Summary",
    "servicesIncluded": "Services Included",
    "allFeesIncluded": "Price includes all fees",
    "jurisdictionConfirm": "I confirm I can operate in this jurisdiction",
    "termsAccept": "I agree to the platform terms",
    "submit": "Submit Proposal",
    "success": "Bid submitted successfully!",
    "error": "Failed to submit bid"
  },
  "auth": {
    "loginTitle": "Welcome Back",
    "registerTitle": "Create Your Account",
    "email": "Email",
    "password": "Password",
    "confirmPassword": "Confirm Password",
    "fullName": "Full Name",
    "phone": "Phone Number",
    "companyName": "Company Name",
    "industry": "Industry",
    "accountantRole": "I'm an Accountant",
    "clientRole": "I'm a Company",
    "loginBtn": "Sign In",
    "registerBtn": "Create Account",
    "noAccount": "Don't have an account?",
    "haveAccount": "Already have an account?",
    "registerLink": "Register",
    "loginLink": "Login"
  },
  "dashboard": {
    "title": "Dashboard",
    "totalBids": "Total Bids",
    "pendingBids": "Pending",
    "acceptedBids": "Accepted",
    "profileComplete": "Profile Complete",
    "recentBids": "Recent Bids",
    "totalJobs": "Total Jobs",
    "activeJobs": "Active Jobs",
    "bidsReceived": "Bids Received"
  },
  "common": {
    "save": "Save",
    "cancel": "Cancel",
    "edit": "Edit",
    "delete": "Delete",
    "create": "Create",
    "update": "Update",
    "confirm": "Confirm",
    "close": "Close",
    "back": "Back",
    "loading": "Loading...",
    "noResults": "No results found",
    "noBids": "No bids yet",
    "noJobs": "No jobs found",
    "page": "Page",
    "of": "of",
    "search": "Search",
    "clear": "Clear",
    "actions": "Actions",
    "success": "Success",
    "error": "Error"
  },
  "theme": {
    "light": "Light",
    "dark": "Dark"
  },
  "language": {
    "en": "English",
    "ar": "العربية"
  }
}
'''

AR_JSON = '''
{
  "nav": {
    "browseJobs": "تصفح الوظائف",
    "dashboard": "لوحة التحكم",
    "myBids": "عروضي",
    "myJobs": "وظائفي",
    "profile": "الملف الشخصي",
    "login": "تسجيل الدخول",
    "register": "إنشاء حساب",
    "logout": "تسجيل الخروج",
    "postJob": "نشر وظيفة",
    "admin": "لوحة الإدارة"
  },
  "hero": {
    "title": "ابحث عن وظائف المحاسبة",
    "subtitle": "تصفح مئات فرص المحاسبة والمالية من شركات موثوقة"
  },
  "jobCard": {
    "budget": "الميزانية",
    "deadline": "الموعد النهائي",
    "bids": "عروض",
    "posted": "نشرت",
    "open": "مفتوح",
    "closed": "مغلق",
    "viewDetails": "عرض التفاصيل"
  },
  "filters": {
    "title": "التصفية",
    "search": "ابحث عن وظائف...",
    "category": "الفئة",
    "budgetRange": "نطاق الميزانية",
    "standard": "المعيار المحاسبي",
    "jurisdiction": "الاختصاص",
    "status": "الحالة",
    "all": "الكل",
    "openOnly": "مفتوح فقط",
    "closedOnly": "مغلق فقط",
    "sortBy": "ترتيب حسب",
    "newest": "الأحدث",
    "highestBudget": "أعلى ميزانية",
    "mostBids": "الأكثر عروضاً",
    "clearAll": "مسح التصفية"
  },
  "jobDetail": {
    "budget": "الميزانية",
    "deadline": "الموعد النهائي",
    "delivery": "التسليم المتوقع",
    "bidsReceived": "العروض المستلمة",
    "requiredSkills": "المهارات المطلوبة",
    "certifications": "الشهادات",
    "software": "البرامج",
    "standard": "المعيار",
    "jurisdiction": "الاختصاص",
    "attachments": "المرفقات",
    "noAttachments": "لا توجد مرفقات",
    "submitBid": "تقديم عرض",
    "alreadyBid": "لقد قدمت عرضاً",
    "jobClosed": "هذه الوظيفة مغلقة",
    "ndaRequired": "مطلوب اتفاقية سرية",
    "acceptNda": "قبول الاتفاقية لعرض التفاصيل",
    "matchScore": "نسبة التطابق"
  },
  "bidForm": {
    "title": "تقديم العرض",
    "price": "السعر المقترح",
    "pricingModel": "نموذج التسعير",
    "fixed": "سعر ثابت",
    "hourly": "بالساعة",
    "retainer": "راتب شهري",
    "deliveryTime": "وقت التسليم المتوقع",
    "estimatedHours": "الساعات المقدرة",
    "coverLetter": "رسالة التغطية / العرض",
    "experience": "ملخص الخبرة ذات الصلة",
    "servicesIncluded": "الخدمات المشمولة",
    "allFeesIncluded": "السعر يشمل جميع الرسوم",
    "jurisdictionConfirm": "أؤكد قدرتي على العمل في هذا الاختصاص",
    "termsAccept": "أوافق على شروط المنصة",
    "submit": "تقديم العرض",
    "success": "تم تقديم العرض بنجاح!",
    "error": "فشل تقديم العرض"
  },
  "auth": {
    "loginTitle": "مرحباً بعودتك",
    "registerTitle": "إنشاء حسابك",
    "email": "البريد الإلكتروني",
    "password": "كلمة المرور",
    "confirmPassword": "تأكيد كلمة المرور",
    "fullName": "الاسم الكامل",
    "phone": "رقم الهاتف",
    "companyName": "اسم الشركة",
    "industry": "الصناعة",
    "accountantRole": "أنا محاسب",
    "clientRole": "أنا شركة",
    "loginBtn": "تسجيل الدخول",
    "registerBtn": "إنشاء حساب",
    "noAccount": "ليس لديك حساب؟",
    "haveAccount": "لديك حساب بالفعل؟",
    "registerLink": "سجل الآن",
    "loginLink": "سجل الدخول"
  },
  "dashboard": {
    "title": "لوحة التحكم",
    "totalBids": "إجمالي العروض",
    "pendingBids": "قيد الانتظار",
    "acceptedBids": "مقبولة",
    "profileComplete": "اكتمال الملف",
    "recentBids": "العروض الأخيرة",
    "totalJobs": "إجمالي الوظائف",
    "activeJobs": "وظائف نشطة",
    "bidsReceived": "العروض المستلمة"
  },
  "common": {
    "save": "حفظ",
    "cancel": "إلغاء",
    "edit": "تعديل",
    "delete": "حذف",
    "create": "إنشاء",
    "update": "تحديث",
    "confirm": "تأكيد",
    "close": "إغلاق",
    "back": "رجوع",
    "loading": "جار التحميل...",
    "noResults": "لا توجد نتائج",
    "noBids": "لا توجد عروض بعد",
    "noJobs": "لم يتم العثور على وظائف",
    "page": "صفحة",
    "of": "من",
    "search": "بحث",
    "clear": "مسح",
    "actions": "إجراءات",
    "success": "تم بنجاح",
    "error": "خطأ"
  },
  "theme": {
    "light": "فاتح",
    "dark": "داكن"
  },
  "language": {
    "en": "English",
    "ar": "العربية"
  }
}
'''

USE_AUTH = '''
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
'''

USE_THEME = '''
import { useState, useEffect } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('ah_theme') || 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('ah_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return { theme, toggleTheme, isDark: theme === 'dark' };
}
'''

USE_LANGUAGE = '''
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';

export function useLanguage() {
  const { i18n } = useTranslation();

  useEffect(() => {
    document.documentElement.setAttribute('dir', i18n.language === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', i18n.language);
  }, [i18n.language]);

  const toggleLanguage = () => {
    const next = i18n.language === 'en' ? 'ar' : 'en';
    i18n.changeLanguage(next);
    localStorage.setItem('ah_lang', next);
  };

  return {
    language: i18n.language,
    toggleLanguage,
    isRTL: i18n.language === 'ar',
  };
}
'''

USE_DEBOUNCE = '''
import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
'''

AUTH_CONTEXT = '''
import { createContext, useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = sessionStorage.getItem('ah_token');
    if (savedToken) {
      setToken(savedToken);
      authService.getMe()
        .then((userData) => setUser(userData))
        .catch(() => {
          sessionStorage.removeItem('ah_token');
          setToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    const response = await authService.login(email, password);
    sessionStorage.setItem('ah_token', response.access_token);
    setToken(response.access_token);
    setUser(response.user);
    return response;
  }, []);

  const register = useCallback(async (data) => {
    const response = await authService.register(data);
    return response;
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem('ah_token');
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated: !!token,
    role: user?.role || null,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
'''

TOAST_CONTEXT = '''
import { createContext, useState, useCallback } from 'react';

export const ToastContext = createContext(null);

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'success') => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = {
    success: (msg) => addToast(msg, 'success'),
    error: (msg) => addToast(msg, 'error'),
    info: (msg) => addToast(msg, 'info'),
  };

  return (
    <ToastContext.Provider value={{ toasts, removeToast, toast }}>
      {children}
    </ToastContext.Provider>
  );
}
'''

API_SERVICE = '''
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('ah_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      sessionStorage.removeItem('ah_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
'''

AUTH_SERVICE = '''
import api from './api';

export const authService = {
  async login(email, password) {
    const { data } = await api.post('/auth/login', { email, password });
    return data;
  },

  async register(userData) {
    const { data } = await api.post('/auth/register', userData);
    return data;
  },

  async getMe() {
    const token = sessionStorage.getItem('ah_token');
    if (!token) return null;
    const { data } = await api.get('/my-profile');
    return data.data;
  },
};
'''

JOB_SERVICE = '''
import api from './api';

export const jobService = {
  async getJobs(params = {}) {
    const { data } = await api.get('/jobs', { params });
    return data;
  },

  async getJob(id) {
    const { data } = await api.get(`/jobs/${id}`);
    return data;
  },

  async getCategories() {
    const { data } = await api.get('/categories');
    return data.data;
  },

  async getCertifications() {
    const { data } = await api.get('/certifications');
    return data.data;
  },

  async getCountries() {
    const { data } = await api.get('/countries');
    return data.data;
  },

  async getContent(key) {
    const { data } = await api.get(`/content/${key}`);
    return data.data;
  },
};
'''

BID_SERVICE = '''
import api from './api';

export const bidService = {
  async submitBid(jobId, bidData) {
    const { data } = await api.post(`/jobs/${jobId}/bids`, bidData);
    return data;
  },

  async getMyBids(page = 1) {
    const { data } = await api.get('/my-bids', { params: { page } });
    return data;
  },

  async acceptNda(jobId) {
    const { data } = await api.post(`/jobs/${jobId}/accept-nda`, { agree: true });
    return data;
  },

  async getMatchScore(jobId) {
    const { data } = await api.get(`/jobs/${jobId}/match-score`);
    return data.data;
  },
};
'''

PROFILE_SERVICE = '''
import api from './api';

export const profileService = {
  async getProfile() {
    const { data } = await api.get('/my-profile');
    return data.data;
  },

  async updateProfile(profileData) {
    const { data } = await api.put('/my-profile', profileData);
    return data;
  },

  async uploadDocument(formData) {
    const { data } = await api.post('/my-profile/documents', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },

  async getDocuments() {
    const { data } = await api.get('/my-profile/documents');
    return data.data;
  },

  async deleteDocument(id) {
    const { data } = await api.delete(`/my-profile/documents/${id}`);
    return data;
  },
};

export const clientService = {
  async getMyJobs(page = 1) {
    const { data } = await api.get('/my-jobs', { params: { page } });
    return data;
  },

  async createJob(jobData) {
    const { data } = await api.post('/my-jobs', jobData);
    return data;
  },

  async updateJob(id, jobData) {
    const { data } = await api.put(`/my-jobs/${id}`, jobData);
    return data;
  },

  async updateJobStatus(id, status, closedReason = null) {
    const { data } = await api.patch(`/my-jobs/${id}/status`, { status, closed_reason: closedReason });
    return data;
  },

  async getJobBids(jobId) {
    const { data } = await api.get(`/my-jobs/${jobId}/bids`);
    return data.data;
  },

  async acceptBid(jobId, bidId) {
    const { data } = await api.patch(`/my-jobs/${jobId}/bids/${bidId}/accept`);
    return data;
  },

  async rejectBid(jobId, bidId) {
    const { data } = await api.patch(`/my-jobs/${jobId}/bids/${bidId}/reject`);
    return data;
  },
};
'''

ADMIN_SERVICE = '''
import api from './api';

export const adminService = {
  getStats: async () => {
    const { data } = await api.get('/admin/dashboard/stats');
    return data.data;
  },

  // Generic CRUD helpers
  list: async (resource, params = {}) => {
    const { data } = await api.get(`/admin/${resource}`, { params });
    return data;
  },

  get: async (resource, id) => {
    const { data } = await api.get(`/admin/${resource}/${id}`);
    return data.data;
  },

  create: async (resource, body) => {
    const { data } = await api.post(`/admin/${resource}`, body);
    return data;
  },

  update: async (resource, id, body) => {
    const { data } = await api.put(`/admin/${resource}/${id}`, body);
    return data;
  },

  remove: async (resource, id) => {
    const { data } = await api.delete(`/admin/${resource}/${id}`);
    return data;
  },

  // Audit log specific
  getAuditLogs: async (params = {}) => {
    const { data } = await api.get('/admin/audit-logs', { params });
    return data;
  },

  getAuditLog: async (id) => {
    const { data } = await api.get(`/admin/audit-logs/${id}`);
    return data.data;
  },

  getAuditFilters: async () => {
    const { data } = await api.get('/admin/audit-logs/meta/filters');
    return data.data;
  },

  // Audit toggle
  getAuditToggle: async () => {
    const { data } = await api.get('/admin/me/audit-toggle');
    return data;
  },

  toggleAudit: async (enabled) => {
    const { data } = await api.patch('/admin/me/audit-toggle', { audit_enabled: enabled });
    return data;
  },

  // Restrictions
  getRestrictions: async (userId) => {
    const { data } = await api.get(`/admin/users/${userId}/restrictions`);
    return data;
  },

  setRestrictions: async (userId, restrictions) => {
    const { data } = await api.patch(`/admin/users/${userId}/restrictions`, restrictions);
    return data;
  },

  removeRestrictions: async (userId) => {
    const { data } = await api.delete(`/admin/users/${userId}/restrictions`);
    return data;
  },
};
'''

FORMAT_DATE = '''
import { formatDistanceToNow, format, isToday, isYesterday } from 'date-fns';

export function formatRelativeDate(dateString) {
  const date = new Date(dateString);
  if (isToday(date)) return 'Today';
  if (isYesterday(date)) return 'Yesterday';
  return formatDistanceToNow(date, { addSuffix: true });
}

export function formatDeadline(dateString) {
  const date = new Date(dateString);
  return format(date, 'MMM dd, yyyy');
}

export function formatFullDate(dateString) {
  const date = new Date(dateString);
  return format(date, 'MMMM dd, yyyy');
}
'''

FORMAT_CURRENCY = '''
export function formatCurrency(amount, currency = 'USD') {
  if (amount == null) return '—';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatBudgetRange(min, max, currency = 'USD') {
  return `${formatCurrency(min, currency)} - ${formatCurrency(max, currency)}`;
}
'''

CONSTANTS = '''
export const ROLES = {
  ADMIN: 'admin',
  CLIENT: 'client',
  ACCOUNTANT: 'accountant',
};

export const JOB_STATUS = {
  OPEN: 'open',
  CLOSED: 'closed',
};

export const BID_STATUS = {
  PENDING: 'pending',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
};

export const PRICING_MODELS = [
  { value: 'fixed', label: 'Fixed Price' },
  { value: 'hourly', label: 'Hourly' },
  { value: 'retainer', label: 'Retainer' },
];

export const ENGAGEMENT_TYPES = [
  { value: 'one_time', label: 'One-Time' },
  { value: 'recurring', label: 'Recurring' },
];

export const SORT_OPTIONS = [
  { value: 'newest', label: 'Newest' },
  { value: 'budget_high', label: 'Highest Budget' },
  { value: 'budget_low', label: 'Lowest Budget' },
  { value: 'bids', label: 'Most Bids' },
  { value: 'deadline', label: 'Deadline' },
];
'''

BUTTON_JSX = '''
import { Spinner } from './Spinner';
import './Button.css';

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  ...props
}) {
  return (
    <button
      type={type}
      className={`btn btn-${variant} btn-${size} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading && <Spinner size="sm" />}
      <span className={loading ? 'btn-text-hidden' : ''}>{children}</span>
    </button>
  );
}
'''

INPUT_JSX = '''
import './Input.css';

export function Input({
  label,
  placeholder,
  value,
  onChange,
  error,
  hint,
  disabled,
  prefix,
  suffix,
  type = 'text',
  name,
  required,
  ...props
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <div className="input-wrapper">
        {prefix && <span className="input-prefix">{prefix}</span>}
        <input
          id={name}
          name={name}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className="input-field"
          required={required}
          {...props}
        />
        {suffix && <span className="input-suffix">{suffix}</span>}
      </div>
      {error && <span className="input-error-text">{error}</span>}
      {hint && !error && <span className="input-hint">{hint}</span>}
    </div>
  );
}
'''

SELECT_JSX = '''
import './Input.css';

export function Select({
  label,
  options = [],
  value,
  onChange,
  error,
  placeholder = 'Select...',
  name,
  required,
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <div className="input-wrapper">
        <select
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          className="input-field select-field"
          required={required}
        >
          <option value="">{placeholder}</option>
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <span className="select-chevron">▾</span>
      </div>
      {error && <span className="input-error-text">{error}</span>}
    </div>
  );
}
'''

TEXTAREA_JSX = '''
import './Input.css';

export function Textarea({
  label,
  placeholder,
  value,
  onChange,
  error,
  rows = 4,
  maxLength,
  name,
  required,
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <textarea
        id={name}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        rows={rows}
        maxLength={maxLength}
        className="input-field textarea-field"
        required={required}
      />
      <div className="textarea-footer">
        {error && <span className="input-error-text">{error}</span>}
        {maxLength && (
          <span className="char-count">{value?.length || 0}/{maxLength}</span>
        )}
      </div>
    </div>
  );
}
'''

BADGE_JSX = '''
import './Badge.css';

export function Badge({ variant = 'neutral', children }) {
  return <span className={`badge badge-${variant}`}>{children}</span>;
}
'''

CARD_JSX = '''
import './Card.css';

export function Card({ children, onClick, hoverable = false, padding = 'md', className = '' }) {
  return (
    <div
      className={`card card-padding-${padding} ${hoverable ? 'card-hoverable' : ''} ${className}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      {children}
    </div>
  );
}
'''

MODAL_JSX = '''
import { useEffect, useRef } from 'react';
import './Modal.css';

export function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  const overlayRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleOverlayClick = (e) => {
    if (e.target === overlayRef.current) onClose();
  };

  return (
    <div className="modal-overlay animate-fade-in" ref={overlayRef} onClick={handleOverlayClick}>
      <div className={`modal-content modal-${size} animate-scale-in`}>
        <div className="modal-header">
          <h2>{title}</h2>
          <button className="modal-close" onClick={onClose} aria-label="Close">✕</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}
'''

SKELETON_JSX = '''
import './Skeleton.css';

export function Skeleton({ width, height, variant = 'text' }) {
  return (
    <div
      className={`skeleton skeleton-${variant}`}
      style={{ width: width || '100%', height: height || '16px' }}
    />
  );
}
'''

PAGINATION_JSX = '''
import { useTranslation } from 'react-i18next';
import './Pagination.css';

export function Pagination({ page, totalPages, onPageChange }) {
  const { t } = useTranslation();
  if (totalPages <= 1) return null;

  const pages = [];
  const maxVisible = 5;
  let start = Math.max(1, page - Math.floor(maxVisible / 2));
  let end = Math.min(totalPages, start + maxVisible - 1);
  if (end - start < maxVisible - 1) start = Math.max(1, end - maxVisible + 1);

  for (let i = start; i <= end; i++) pages.push(i);

  return (
    <div className="pagination">
      <button className="pagination-btn" disabled={page === 1} onClick={() => onPageChange(page - 1)}>‹</button>
      {start > 1 && <><button className="pagination-btn" onClick={() => onPageChange(1)}>1</button><span className="pagination-ellipsis">…</span></>}
      {pages.map((p) => (
        <button key={p} className={`pagination-btn ${p === page ? 'active' : ''}`} onClick={() => onPageChange(p)}>{p}</button>
      ))}
      {end < totalPages && <><span className="pagination-ellipsis">…</span><button className="pagination-btn" onClick={() => onPageChange(totalPages)}>{totalPages}</button></>}
      <button className="pagination-btn" disabled={page === totalPages} onClick={() => onPageChange(page + 1)}>›</button>
    </div>
  );
}
'''

SEARCHBAR_JSX = '''
import { useTranslation } from 'react-i18next';
import './SearchBar.css';

export function SearchBar({ value, onChange, onSearch, placeholder }) {
  const { t } = useTranslation();

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && onSearch) onSearch(value);
  };

  return (
    <div className="search-bar">
      <span className="search-icon">🔍</span>
      <input
        type="text"
        className="search-input"
        placeholder={placeholder || t('filters.search')}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      {value && (
        <button className="search-clear" onClick={() => onChange('')}>✕</button>
      )}
    </div>
  );
}
'''

EMPTYSTATE_JSX = '''
import { Button } from './Button';
import './EmptyState.css';

export function EmptyState({ icon = '📋', title, description, action }) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">{icon}</div>
      <h3 className="empty-state-title">{title}</h3>
      {description && <p className="empty-state-description">{description}</p>}
      {action && (
        <Button variant="primary" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  );
}
'''

TOAST_JSX = '''
import { useContext } from 'react';
import { ToastContext } from '../../context/ToastContext';
import './Toast.css';

export function ToastContainer() {
  const { toasts, removeToast } = useContext(ToastContext);

  if (toasts.length === 0) return null;

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast-${toast.type} animate-slide-right`}>
          <span className="toast-icon">
            {toast.type === 'success' && '✅'}
            {toast.type === 'error' && '❌'}
            {toast.type === 'info' && 'ℹ️'}
          </span>
          <span className="toast-message">{toast.message}</span>
          <button className="toast-close" onClick={() => removeToast(toast.id)}>✕</button>
        </div>
      ))}
    </div>
  );
}
'''

SPINNER_JSX = '''
import './Spinner.css';

export function Spinner({ size = 'md', color }) {
  return (
    <div
      className={`spinner spinner-${size}`}
      style={color ? { borderTopColor: color } : undefined}
    />
  );
}
'''

MULTISELECT_JSX = '''
import { useState, useRef, useEffect } from 'react';
import './MultiSelect.css';

export function MultiSelect({ label, options = [], selected = [], onChange, placeholder = 'Select...' }) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setIsOpen(false);
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filtered = options.filter((opt) =>
    opt.label.toLowerCase().includes(search.toLowerCase())
  );

  const toggle = (value) => {
    const next = selected.includes(value)
      ? selected.filter((v) => v !== value)
      : [...selected, value];
    onChange(next);
  };

  const remove = (value) => {
    onChange(selected.filter((v) => v !== value));
  };

  return (
    <div className="multiselect" ref={ref}>
      {label && <label className="input-label">{label}</label>}
      <div className="multiselect-trigger" onClick={() => setIsOpen(!isOpen)}>
        <div className="multiselect-chips">
          {selected.length === 0 && <span className="multiselect-placeholder">{placeholder}</span>}
          {selected.map((val) => {
            const opt = options.find((o) => o.value === val);
            return (
              <span key={val} className="multiselect-chip">
                {opt?.label || val}
                <button onClick={(e) => { e.stopPropagation(); remove(val); }}>✕</button>
              </span>
            );
          })}
        </div>
        <span className="select-chevron">▾</span>
      </div>
      {isOpen && (
        <div className="multiselect-dropdown animate-fade-in">
          <input
            type="text"
            className="multiselect-search"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onClick={(e) => e.stopPropagation()}
          />
          <div className="multiselect-options">
            {filtered.map((opt) => (
              <label key={opt.value} className="multiselect-option">
                <input
                  type="checkbox"
                  checked={selected.includes(opt.value)}
                  onChange={() => toggle(opt.value)}
                />
                <span>{opt.label}</span>
              </label>
            ))}
            {filtered.length === 0 && <div className="multiselect-no-results">No results</div>}
          </div>
        </div>
      )}
    </div>
  );
}
'''

DISCLAIMER_BANNER_JSX = '''
import { Button } from './Button';
import './DisclaimerBanner.css';

export function DisclaimerBanner({ title, text, onAccept, onDecline, acceptLabel = 'Accept', declineLabel = 'Decline' }) {
  return (
    <div className="disclaimer-banner animate-fade-in">
      <div className="disclaimer-content">
        <h3>{title}</h3>
        <div className="disclaimer-text">{text}</div>
        <div className="disclaimer-actions">
          <Button variant="primary" onClick={onAccept}>{acceptLabel}</Button>
          {onDecline && <Button variant="ghost" onClick={onDecline}>{declineLabel}</Button>}
        </div>
      </div>
    </div>
  );
}
'''

NAVBAR_JSX = '''
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTheme } from '../../hooks/useTheme';
import { useLanguage } from '../../hooks/useLanguage';
import { Button } from '../ui/Button';
import './Navbar.css';

export function Navbar() {
  const { t } = useTranslation();
  const { isAuthenticated, role, user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          Accountant<span className="logo-green">Hub</span>
        </Link>

        <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
          <Link to="/" onClick={() => setMenuOpen(false)}>{t('nav.browseJobs')}</Link>

          {isAuthenticated && role === 'accountant' && (
            <>
              <Link to="/dashboard" onClick={() => setMenuOpen(false)}>{t('nav.dashboard')}</Link>
              <Link to="/my-bids" onClick={() => setMenuOpen(false)}>{t('nav.myBids')}</Link>
            </>
          )}

          {isAuthenticated && role === 'client' && (
            <>
              <Link to="/client/dashboard" onClick={() => setMenuOpen(false)}>{t('nav.dashboard')}</Link>
              <Link to="/client/jobs/new" onClick={() => setMenuOpen(false)}>{t('nav.postJob')}</Link>
            </>
          )}

          {isAuthenticated && role === 'admin' && (
            <Link to="/admin" onClick={() => setMenuOpen(false)}>{t('nav.admin')}</Link>
          )}
        </div>

        <div className="navbar-actions">
          <button className="nav-icon-btn" onClick={toggleTheme} title={t(`theme.${theme}`)}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          <button className="nav-icon-btn" onClick={toggleLanguage} title={t(`language.${language}`)}>
            {language === 'en' ? 'AR' : 'EN'}
          </button>

          {isAuthenticated ? (
            <div className="navbar-user">
              <Link to={role === 'client' ? '/client/profile' : '/profile'} className="nav-user-link">
                <span className="nav-avatar">👤</span>
                <span className="nav-username">{user?.name}</span>
              </Link>
              <Button variant="ghost" size="sm" onClick={handleLogout}>{t('nav.logout')}</Button>
            </div>
          ) : (
            <div className="navbar-auth">
              <Link to="/login"><Button variant="ghost" size="sm">{t('nav.login')}</Button></Link>
              <Link to="/register"><Button variant="primary" size="sm">{t('nav.register')}</Button></Link>
            </div>
          )}

          <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>
    </nav>
  );
}
'''

FOOTER_JSX = '''
import { Link } from 'react-router-dom';
import './Footer.css';

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="footer-logo">Accountant<span className="logo-green">Hub</span></span>
          <p className="footer-disclaimer">
            Accountant Hub is a marketplace connecting businesses with independent accounting professionals.
            We do not employ or guarantee the work of any professional.
          </p>
        </div>
        <div className="footer-links">
          <Link to="/">Browse Jobs</Link>
          <a href="#">Terms of Service</a>
          <a href="#">Privacy Policy</a>
        </div>
      </div>
    </footer>
  );
}
'''

SIDEBAR_JSX = '''
import { useTranslation } from 'react-i18next';
import './Sidebar.css';

export function Sidebar({ filters, onFilterChange, onClear, isOpen, onClose }) {
  const { t } = useTranslation();

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <h3>{t('filters.title')}</h3>
          <button className="sidebar-close" onClick={onClose}>✕</button>
        </div>
        <div className="sidebar-body">
          {/* Category */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.category')}</label>
            <select
              className="input-field select-field"
              value={filters.category || ''}
              onChange={(e) => onFilterChange('category', e.target.value)}
            >
              <option value="">{t('filters.all')}</option>
              {filters.categories?.map((cat) => (
                <option key={cat.slug} value={cat.slug}>{cat.name}</option>
              ))}
            </select>
          </div>

          {/* Budget Range */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.budgetRange')}</label>
            <div className="filter-range">
              <input type="number" className="input-field" placeholder="Min"
                value={filters.budget_min || ''} onChange={(e) => onFilterChange('budget_min', e.target.value)} />
              <span>—</span>
              <input type="number" className="input-field" placeholder="Max"
                value={filters.budget_max || ''} onChange={(e) => onFilterChange('budget_max', e.target.value)} />
            </div>
          </div>

          {/* Standard */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.standard')}</label>
            <select className="input-field select-field"
              value={filters.accounting_standard || ''}
              onChange={(e) => onFilterChange('accounting_standard', e.target.value)}>
              <option value="">{t('filters.all')}</option>
              <option value="GAAP">GAAP</option>
              <option value="IFRS">IFRS</option>
              <option value="Local GAAP">Local GAAP</option>
            </select>
          </div>

          {/* Jurisdiction */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.jurisdiction')}</label>
            <input type="text" className="input-field" placeholder="US, UK, UAE..."
              value={filters.jurisdiction || ''} onChange={(e) => onFilterChange('jurisdiction', e.target.value)} />
          </div>

          {/* Status */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.status')}</label>
            <select className="input-field select-field"
              value={filters.status || 'open'}
              onChange={(e) => onFilterChange('status', e.target.value)}>
              <option value="open">{t('filters.openOnly')}</option>
              <option value="closed">{t('filters.closedOnly')}</option>
              <option value="">{t('filters.all')}</option>
            </select>
          </div>

          {/* Sort */}
          <div className="filter-group">
            <label className="filter-label">{t('filters.sortBy')}</label>
            <select className="input-field select-field"
              value={filters.sort || 'newest'}
              onChange={(e) => onFilterChange('sort', e.target.value)}>
              <option value="newest">{t('filters.newest')}</option>
              <option value="budget_high">{t('filters.highestBudget')}</option>
              <option value="bids">{t('filters.mostBids')}</option>
            </select>
          </div>
        </div>
        <div className="sidebar-footer">
          <button className="btn btn-ghost btn-md" onClick={onClear}>{t('filters.clearAll')}</button>
        </div>
      </aside>
    </>
  );
}
'''

LAYOUT_JSX = '''
import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { ToastContainer } from '../ui/Toast';
import './Layout.css';

export function Layout() {
  return (
    <div className="layout">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <Footer />
      <ToastContainer />
    </div>
  );
}
'''

PROTECTED_ROUTE_JSX = '''
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export function ProtectedRoute({ role }) {
  const { isAuthenticated, role: userRole, isLoading } = useAuth();

  if (isLoading) {
    return <div className="loading-screen">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (role && userRole !== role) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
'''

APP_JSX = '''
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import JobListPage from './pages/public/JobListPage';
import JobDetailPage from './pages/public/JobDetailPage';
import LoginPage from './pages/public/LoginPage';
import RegisterPage from './pages/public/RegisterPage';

export default function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            {/* Public */}
            <Route index element={<JobListPage />} />
            <Route path="jobs/:id" element={<JobDetailPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />

            {/* Pages will be added in Phase II setup */}
          </Route>
        </Routes>
      </ToastProvider>
    </AuthProvider>
  );
}
'''

MAIN_JSX = '''
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App';
import './i18n';
import './styles/theme.css';
import './styles/global.css';
import './styles/animations.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
'''

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("ACCOUNTANT HUB - FRONTEND SETUP PHASE I")
    print("="*60)
    os.chdir(BASE_DIR)

    setup_theme_and_styles()
    setup_i18n()
    setup_hooks()
    setup_context()
    setup_services()
    setup_utils()
    setup_ui_components()
    setup_layout()
    setup_app_entry()

    print_summary()