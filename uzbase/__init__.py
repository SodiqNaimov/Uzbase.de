import os
import secrets
from flask import Flask, session, request, redirect, url_for
from uzbase.models import db

# Multilingual Translations dictionary
TRANSLATIONS = {
    'uz': {
        'brand': 'UZBASE',
        'tagline': "Germaniyadagi O'zbeklar hamjamiyati",
        'jobs': 'Ishlar',
        'housing': 'Turar joy',
        'community': 'Hamjamiyat',
        'info': 'Ma\'lumotlar',
        'services': 'Xizmatlar',
        'post_job': 'E\'lon joylash',
        'post_house': 'E\'lon joylash',
        'search': 'Qidirish...',
        'city': 'Shahar',
        'category': 'Turkum',
        'all': 'Barchasi',
        'price': 'Narxi',
        'availability': 'Sana',
        'size': 'Maydoni',
        'author': 'Muallif',
        'replies': 'Javoblar',
        'upvotes': 'Ovozlar',
        'write_comment': 'Fikr bildirish...',
        'add_comment': 'Fikr qo\'shish',
        'recent_posts': 'So\'nggi e\'lonlar',
        'contact': 'Aloqa',
        'telegram': 'Telegram orqali bog\'lanish',
        'verified': 'Tasdiqlangan',
        'search_placeholder': 'Kalit so\'zlar bo\'yicha qidirish',
        'location': 'Joylashuv',
        'description': 'Tavsif',
        'submit': 'Yuborish',
        'cancel': 'Bekor qilish',
        'add_new': 'Yangi qo\'shish',
        'bureaucracy': 'Germaniya Byurokratiyasi',
        'legal_help': 'Huquqiy maslahat',
        'translations_service': 'Tarjimonlar',
        'leaders': 'Faollar va Uyushmalar',
        'empty_results': 'Hech narsa topilmadi.',
        'all_cities': 'Barcha shaharlar',
        'any_date': 'Istalgan vaqt',
        'login': 'Kirish',
        'register': 'Ro\'yxatdan o\'tish',
        'logout': 'Chiqish',
        'cabinet': 'Shaxsiy Kabinet',
        'username': 'Foydalanuvchi nomi',
        'password': 'Parol',
        'email': 'Elektron pochta',
        'fullname': 'To\'liq ismingiz',
        'confirm_password': 'Parolni tasdiqlang',
        'back_home': 'Bosh sahifaga qaytish',
        'security_warning': 'Xavfsizlik ogohlantirishi: parolingiz kamida 8 ta belgidan iborat bo\'lishi va maxsus belgilarni o\'z ichiga olishi kerak.',
        'edit': 'Tahrirlash',
        'delete': 'O\'chirish',
        'save': 'Saqlash',
        
        # Admin Panel Strings
        'admin_panel': 'Admin paneli',
        'control_dashboard': 'UZBASE boshqaruv paneli',
        'dashboard_stats': 'Statistika va tahlil',
        'wiki_categories': 'Wiki turkumlar',
        'wiki_guides': 'Wiki qo\'llanmalar',
        'user_accounts': 'Foydalanuvchilar',
        'classified_listings': 'E\'lonlar boshqaruvi',
        'forum_moderation': 'Forum moderatsiyasi',
        'analytics_overview': 'Tahlil va umumiy ko\'rinish',
        'traffic_metrics': 'UZBASE a\'zolari va tashriflar statistikasi',
        'total_members': 'Jami a\'zolar',
        'page_views_stats': 'Sahifalar ko\'rilishi statistikasi',
        'route_path': 'Yo\'nalish yo\'li (Route)',
        'visits_count': 'Tashriflar soni',
        'add_new_category': 'Yangi turkum qo\'shish',
        'create_category': 'Turkum yaratish',
        'current_categories': 'Mavjud turkumlar',
        'wiki_guide_topics': 'Wiki qo\'llanma mavzulari',
        'create_new_guide': 'Yangi qo\'llanma yaratish',
        'assign_category': 'Turkumni tanlang',
        'active_jobs': 'Faol ish e\'lonlari',
        'active_housing': 'Faol turar joy e\'lonlari',
        'active_forum': 'Faol forum mavzulari',
        'registered_users': 'Ro\'yxatdan o\'tgan a\'zolar',
        'save_changes': 'O\'zgarishlarni saqlash',
        'profile_settings': 'Profil sozlamalari',
        'change_password': 'Parolni o\'zgartirish',
        'my_listings': 'Mening e\'lonlarim',
        'navigation': 'Navigatsiya',
        'current_password': 'Amaldagi parol',
        'new_password': 'Yangi parol',
        'confirm_new_password': 'Yangi parolni tasdiqlang',
        'update_details': 'Ma\'lumotlarni yangilash',
        'my_listings_posts': 'Mening e\'lonlarim va postlarim',
        'jobs_listings': 'Ish e\'lonlari',
        'housing_listings': 'Turar joy e\'lonlari',
        'forum_topics': 'Forum mavzulari',
        'no_listings_yet': 'Siz hali hech qanday e\'lon yoki post joylashtirmadingiz.',
        'search_my_listings': 'E\'lonlarimni qidirish',
        'edit_job': 'Ish e\'lonini tahrirlash',
        'edit_housing': 'Turar joy e\'lonini tahrirlash',
        'edit_topic': 'Mavzuni tahrirlash',
    },
    'de': {
        'brand': 'UZBASE',
        'tagline': 'Ihre Basis in Deutschland',
        'jobs': 'Jobs',
        'housing': 'Unterkunft',
        'community': 'Gemeinschaft',
        'info': 'Info Wiki',
        'services': 'Dienstleistungen',
        'post_job': 'Job inserieren',
        'post_house': 'Wohnung inserieren',
        'search': 'Suchen...',
        'city': 'Stadt',
        'category': 'Kategorie',
        'all': 'Alle',
        'price': 'Preis',
        'availability': 'Verfügbarkeit',
        'size': 'Größe',
        'author': 'Autor',
        'replies': 'Antworten',
        'upvotes': 'Stimmen',
        'write_comment': 'Kommentar schreiben...',
        'add_comment': 'Kommentar hinzufügen',
        'recent_posts': 'Aktuelle Beiträge',
        'contact': 'Kontakt',
        'telegram': 'Über Telegram kontaktieren',
        'verified': 'Verifiziert',
        'search_placeholder': 'Nach Stichworten suchen',
        'location': 'Ort',
        'description': 'Beschreibung',
        'submit': 'Absenden',
        'cancel': 'Abbrechen',
        'add_new': 'Neu hinzufügen',
        'bureaucracy': 'Deutsche Bürokratie',
        'legal_help': 'Rechtsberatung',
        'translations_service': 'Übersetzungen',
        'leaders': 'Aktivisten & Vereine',
        'empty_results': 'Keine Ergebnisse gefunden.',
        'all_cities': 'Alle Städte',
        'any_date': 'Beliebiges Datum',
        'login': 'Anmelden',
        'register': 'Registrieren',
        'logout': 'Abmelden',
        'cabinet': 'Mein Kabinett',
        'username': 'Benutzername',
        'password': 'Passwort',
        'email': 'E-Mail-Adresse',
        'fullname': 'Vollständiger Name',
        'confirm_password': 'Passwort bestätigen',
        'back_home': 'Zur Startseite',
        'security_warning': 'Sicherheitshinweis: Ihr Passwort muss mindestens 8 Zeichen lang sein und Sonderzeichen enthalten.',
        'edit': 'Bearbeiten',
        'delete': 'Löschen',
        'save': 'Speichern',
        
        # Admin Panel Strings
        'admin_panel': 'Admin-Panel',
        'control_dashboard': 'UZBASE Kontroll-Dashboard',
        'dashboard_stats': 'Dashboard & Statistiken',
        'wiki_categories': 'Wiki-Kategorien',
        'wiki_guides': 'Wiki-Leitfäden',
        'user_accounts': 'Benutzerkonten',
        'classified_listings': 'Kleinanzeigen',
        'forum_moderation': 'Forum-Moderation',
        'analytics_overview': 'Analysen & Übersicht',
        'traffic_metrics': 'UZBASE globaler Traffic und Mitgliederkennzahlen',
        'total_members': 'Mitglieder insgesamt',
        'page_views_stats': 'Seitenaufruf-Statistiken',
        'route_path': 'Seitenpfad (Route)',
        'visits_count': 'Aufrufe',
        'add_new_category': 'Neue Kategorie hinzufügen',
        'create_category': 'Kategorie erstellen',
        'current_categories': 'Aktuelle Kategorien',
        'wiki_guide_topics': 'Wiki-Leitfaden-Themen',
        'create_new_guide': 'Neuen Wiki-Leitfaden erstellen',
        'assign_category': 'Kategorie zuweisen',
        'active_jobs': 'Aktive Jobanzeigen',
        'active_housing': 'Aktive Wohnungsanzeigen',
        'active_forum': 'Aktive Forumthemen',
        'registered_users': 'Registrierte Benutzer',
        'save_changes': 'Änderungen speichern',
        'profile_settings': 'Profileinstellungen',
        'change_password': 'Kennwort ändern',
        'my_listings': 'Meine Anzeigen',
        'navigation': 'Navigation',
        'current_password': 'Aktuelles Passwort',
        'new_password': 'Neues Passwort',
        'confirm_new_password': 'Neues Passwort bestätigen',
        'update_details': 'Details aktualisieren',
        'my_listings_posts': 'Meine Anzeigen & Beiträge',
        'jobs_listings': 'Stellenanzeigen',
        'housing_listings': 'Wohnungsanzeigen',
        'forum_topics': 'Forumthemen',
        'no_listings_yet': 'Sie haben noch keine Anzeigen veröffentlicht.',
        'search_my_listings': 'Meine Anzeigen durchsuchen',
        'edit_job': 'Stellenanzeige bearbeiten',
        'edit_housing': 'Wohnungsanzeige bearbeiten',
        'edit_topic': 'Thema bearbeiten',
    },
    'ru': {
        'brand': 'UZBASE',
        'tagline': 'Ваша база в Германии',
        'jobs': 'Работа',
        'housing': 'Жилье',
        'community': 'Сообщество',
        'info': 'Инфо Вики',
        'services': 'Услуги',
        'post_job': 'Разместить вакансию',
        'post_house': 'Разместить жилье',
        'search': 'Поиск...',
        'city': 'Город',
        'category': 'Категория',
        'all': 'Все',
        'price': 'Цена',
        'availability': 'Доступно с',
        'size': 'Площадь',
        'author': 'Автор',
        'replies': 'Ответы',
        'upvotes': 'Голоса',
        'write_comment': 'Написать комментарий...',
        'add_comment': 'Добавить комментарий',
        'recent_posts': 'Свежие объявления',
        'contact': 'Контакты',
        'telegram': 'Связаться через Telegram',
        'verified': 'Подтверждено',
        'search_placeholder': 'Поиск по ключевым словам',
        'location': 'Локация',
        'description': 'Описание',
        'submit': 'Отправить',
        'cancel': 'Отмена',
        'add_new': 'Добавить',
        'bureaucracy': 'Немецкая бюрократия',
        'legal_help': 'Юридическая помощь',
        'translations_service': 'Переводчики',
        'leaders': 'Активисты и диаспоры',
        'empty_results': 'Ничего не найдено.',
        'all_cities': 'Все города',
        'any_date': 'Любая дата',
        'login': 'Войти',
        'register': 'Регистрация',
        'logout': 'Выйти',
        'cabinet': 'Личный кабинет',
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'email': 'Электронная почта',
        'fullname': 'Полное имя',
        'confirm_password': 'Подтвердите пароль',
        'back_home': 'На главную',
        'security_warning': 'Предупреждение безопасности: пароль должен содержать минимум 8 символов и специальные знаки.',
        
        # Admin Panel Strings
        'admin_panel': 'Панель управления',
        'control_dashboard': 'Панель администратора UZBASE',
        'dashboard_stats': 'Статистика',
        'wiki_categories': 'Категории Вики',
        'wiki_guides': 'Руководства Вики',
        'user_accounts': 'Аккаунты пользователей',
        'classified_listings': 'Управление объявлениями',
        'forum_moderation': 'Модерация форума',
        'analytics_overview': 'Аналитика и обзор',
        'traffic_metrics': 'Глобальный трафик UZBASE и показатели участников',
        'total_members': 'Всего участников',
        'page_views_stats': 'Статистика просмотров страниц',
        'route_path': 'Путь страницы (Route)',
        'visits_count': 'Количество визитов',
        'add_new_category': 'Добавить новую категорию',
        'create_category': 'Создать категорию',
        'current_categories': 'Текущие категории',
        'wiki_guide_topics': 'Темы руководств Вики',
        'create_new_guide': 'Создать новое руководство',
        'assign_category': 'Назначить категорию',
        'active_jobs': 'Активные вакансии',
        'active_housing': 'Активные объявления жилья',
        'active_forum': 'Активные темы форума',
        'registered_users': 'Зарегистрированные пользователи',
        'save_changes': 'Сохранить изменения',
        'profile_settings': 'Настройки профиля',
        'change_password': 'Сменить пароль',
        'my_listings': 'Мои объявления',
        'navigation': 'Навигация',
        'current_password': 'Текущий пароль',
        'new_password': 'Новый пароль',
        'confirm_new_password': 'Подтвердите новый пароль',
        'update_details': 'Обновить данные',
        'my_listings_posts': 'Мои объявления и посты',
        'jobs_listings': 'Вакансии',
        'housing_listings': 'Объявления жилья',
        'forum_topics': 'Темы форума',
        'no_listings_yet': 'Вы еще не опубликовали ни одного объявления.',
        'search_my_listings': 'Поиск по моим объявлениям',
        'edit_job': 'Редактировать вакансию',
        'edit_housing': 'Редактировать объявление жилья',
        'edit_topic': 'Редактировать тему',
        'edit': 'Редактировать',
        'delete': 'Удалить',
        'save': 'Сохранить',
    }
}

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuration
    db_path = os.path.join(app.root_path, 'uzbase.db')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'uzbase_germany_secret_key_12345'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False, # Set to True for production HTTPS
        SESSION_COOKIE_SAMESITE='Lax'
    )

    if test_config:
        app.config.from_mapping(test_config)

    # Initialize Database
    db.init_app(app)

    # Multilingual, Translation & Page Tracker Hook
    @app.before_request
    def load_language_and_track():
        if 'lang' not in session:
            session['lang'] = 'uz'

        # Log Page Visit (exclude static and asset files, only count GET pages)
        if request.endpoint and not request.path.startswith('/static') and request.method == 'GET':
            from uzbase.models import PageVisit
            try:
                visit = PageVisit.query.filter_by(path=request.path).first()
                if not visit:
                    visit = PageVisit(path=request.path, count=1)
                    db.session.add(visit)
                else:
                    visit.count += 1
                db.session.commit()
            except Exception:
                db.session.rollback()

    @app.context_processor
    def inject_translations_and_notifications():
        lang = session.get('lang', 'uz')
        ret = {
            'lang': lang,
            't': TRANSLATIONS.get(lang, TRANSLATIONS['uz']),
            'unread_notifications_count': 0,
            'notifications_list': []
        }
        if session.get('username'):
            from uzbase.models import Notification
            try:
                ret['unread_notifications_count'] = Notification.query.filter_by(username=session['username'], is_read=False).count()
                ret['notifications_list'] = Notification.query.filter_by(username=session['username']).order_by(Notification.created_at.desc()).limit(5).all()
            except Exception:
                pass
        return ret

    # CSRF generation hook
    def generate_csrf_token():
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(32)
        return session['csrf_token']

    app.jinja_env.globals['csrf_token'] = generate_csrf_token

    # Register Blueprints
    from uzbase.blueprints.main import main_bp
    from uzbase.blueprints.auth import auth_bp
    from uzbase.blueprints.jobs import jobs_bp
    from uzbase.blueprints.housing import housing_bp
    from uzbase.blueprints.community import community_bp
    from uzbase.blueprints.wiki import wiki_bp
    from uzbase.blueprints.services import services_bp
    from uzbase.blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(housing_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(wiki_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(admin_bp)

    return app
