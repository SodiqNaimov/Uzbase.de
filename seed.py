from uzbase import create_app
from uzbase.models import db, User, Job, Housing, ForumTopic, ForumReply, WikiCategory, WikiItem, Service
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Seed Users
        if not User.query.first():
            print("Seeding Users...")
            admin = User(
                username='admin',
                email='admin@uzbase.de',
                full_name='Administrator',
                password_hash=generate_password_hash('AdminPassword123!'),
                is_admin=True
            )
            sodiq = User(
                username='sodiq',
                email='sodiqnaimov9@gmail.com',
                full_name='Sodiqjon Naimov',
                password_hash=generate_password_hash('Melomon_13!'),
                is_admin=True
            )
            db.session.add_all([admin, sodiq])

        # Seed Jobs
        if not Job.query.first():
            print("Seeding Jobs...")
            jobs = [
                Job(
                    title='Python Backend Developer',
                    company='Berlin Tech Solutions',
                    city='Berlin',
                    salary='€55,000 - €65,000 / year',
                    type='Full-time',
                    category='IT',
                    description='Looking for a junior/mid Python developer comfortable with Flask, Django, and SQLAlchemy. Uzbek language support is a plus for internal communications with Uzbek tech teams.',
                    contact='@berlintech_jobs',
                    email='jobs@berlintech.de',
                    phone='+49 30 123456',
                    author='admin'
                ),
                Job(
                    title='Assistant Sushi Chef / Kitchen Helper',
                    company='Samarkand Restaurant',
                    city='Frankfurt',
                    salary='€14 - €16 / hour',
                    type='Part-time',
                    category='Gastronomy',
                    description='Help prepare ingredients and manage the kitchen. No professional German required. Uzbek/Russian language friendly.',
                    contact='@samarkand_gastronomy',
                    email='kitchen@samarkand-ffm.de',
                    phone=None,
                    author='admin'
                ),
                Job(
                    title='Warehouse Logistics Coordinator',
                    company='DHL Hub Germany',
                    city='Munich',
                    salary='€2,800 / month',
                    type='Full-time',
                    category='Logistics',
                    description='Organize shipping lists, receive packages, and support logistics processes. Basic conversational German (A2) required.',
                    contact='@dhl_munich_hub',
                    email='recruitment@dhl-munich.de',
                    phone='+49 89 9876543',
                    author='admin'
                ),
                Job(
                    title='Student Library Assistant',
                    company='TU Munich Library',
                    city='Munich',
                    salary='€14 / hour',
                    type='Student Jobs',
                    category='Student Jobs',
                    description='Part-time library assistant role. Register books, help students find resources, and manage library orders.',
                    contact='@tum_library_jobs',
                    email='library-jobs@tum.de',
                    phone=None,
                    author='admin'
                )
            ]
            db.session.add_all(jobs)

        # Seed Housing
        if not Housing.query.first():
            print("Seeding Housing...")
            housing = [
                Housing(
                    title='Cozy Student Room (WG) in Berlin-Wedding',
                    type='Room Share (WG)',
                    city='Berlin',
                    price='450',
                    size='18',
                    available_from='01.09.2026',
                    description='A bright room in a shared apartment. 5 minutes walk from U-Bahn. Fully furnished, includes high-speed internet and washing machine.',
                    contact='@berlin_wg_wedding',
                    email='room-wedding@wg-berlin.de',
                    phone='+49 176 99887766',
                    author='admin'
                ),
                Housing(
                    title='Modern 2-Room Apartment near Frankfurt Center',
                    type='Apartment Rental',
                    city='Frankfurt',
                    price='950',
                    size='55',
                    available_from='Immediate',
                    description='Nice apartment with balcony, fully equipped kitchen, separate bedroom. Anmeldung (registration) is possible.',
                    contact='@frankfurt_apt_center',
                    email='info@frankfurt-apartments.de',
                    phone='+49 69 112233',
                    author='admin'
                ),
                Housing(
                    title='Short-term Sublet during Semester Break',
                    type='Short-term Stay',
                    city='Munich',
                    price='400',
                    size='22',
                    available_from='01.08.2026 - 30.09.2026',
                    description='Subletting my student dormitory room while I travel. Fully inclusive price. Only available to matriculated students.',
                    contact='@munich_sublet_student',
                    email='sublet-muc@studentenwerk.de',
                    phone=None,
                    author='admin'
                )
            ]
            db.session.add_all(housing)

        # Seed Forum Topics & Replies
        if not ForumTopic.query.first():
            print("Seeding Forum...")
            topic1 = ForumTopic(
                title='How to get a Tax Number (Steuernummer) for student jobs?',
                category='Studying Here',
                author='sodiq',
                upvotes=12
            )
            topic2 = ForumTopic(
                title='What is the best health insurance (Krankenkasse) for expats?',
                category='Moving to Germany',
                author='admin',
                upvotes=8
            )
            db.session.add_all([topic1, topic2])
            db.session.flush() # Populate IDs

            reply1 = ForumReply(
                topic_id=topic1.id,
                author='admin',
                text='You can apply online via ELSTER or fill out the "Fragebogen zur steuerlichen Erfassung" and mail it to your local Finanzamt!'
            )
            reply2 = ForumReply(
                topic_id=topic1.id,
                author='sodiq',
                text='Thank you! That is very helpful, I will try it today.'
            )
            reply3 = ForumReply(
                topic_id=topic2.id,
                author='sodiq',
                text='TK and AOK are very popular and have English support!'
            )
            db.session.add_all([reply1, reply2, reply3])

        # Seed Wiki Items
        # Seed Wiki Items
        if not WikiItem.query.first():
            print("Seeding Wiki...")
            cat_bureaucracy = WikiCategory(
                name_uz='Germaniya Byurokratiyasi',
                name_de='Deutsche Bürokratie',
                name_ru='Немецкая Бюрократия'
            )
            cat_insurance = WikiCategory(
                name_uz='Tibbiy Sug\'urta',
                name_de='Krankenversicherung',
                name_ru='Медицинское Страхование'
            )
            db.session.add_all([cat_bureaucracy, cat_insurance])
            db.session.commit()

            wiki = [
                WikiItem(
                    title_uz='Steuernummer qanday olinadi',
                    title_de='Wie man eine Steuernummer bekommt',
                    title_ru='Как получить Steuernummer (налоговый номер)',
                    category_id=cat_bureaucracy.id,
                    content_uz='Germaniyada ishlash uchun sizga soliq ID (Steueridentifikationsnummer) va soliq raqami (Steuernummer) kerak. Soliq ID sizning manzilingizni ro\'yxatdan o\'tkazgandan keyin (Anmeldung) pochta orqali yuboriladi. Steuernummer mahalliy Finanzamt-ga ariza topshirish yoki Elster orqali onlayn ariza berish orqali olinadi.',
                    content_de='Um in Deutschland zu arbeiten, benötigen Sie eine Steueridentifikationsnummer und eine Steuernummer. Die Steueridentifikationsnummer wird Ihnen nach der Anmeldung automatisch per Post zugesandt. Die Steuernummer erhalten Sie durch Einreichen eines Formulars beim örtlichen Finanzamt oder durch Online-Beantragung über Elster.',
                    content_ru='Для работы в Германии вам понадобится налоговый ID (Steueridentifikationsnummer) и налоговый номер (Steuernummer). Налоговый ID автоматически высылается вам по почте после регистрации адреса (Anmeldung). Steuernummer можно получить, подав форму в местный Finanzamt или подав заявку онлайн через Elster.'
                ),
                WikiItem(
                    title_uz='Anmeldung (Yashash joyini ro\'yxatga olish) bo\'yicha qo\'llanma',
                    title_de='Anmeldung (Anmeldung einer Wohnung) Leitfaden',
                    title_ru='Руководство по Anmeldung (регистрации по адресу)',
                    category_id=cat_bureaucracy.id,
                    content_uz='Yangi uyga ko\'chib o\'tganingizdan keyin 14 kun ichida mahalliy Bürgeramt-da manzilingizni ro\'yxatdan o\'tkazishingiz kerak. Sizga pasport, to\'ldirilgan ro\'yxatdan o\'tish shakli va uy egasi tasdiqnomasi (Wohnungsgeberbestätigung) kerak bo\'ladi.',
                    content_de='Innerhalb von 14 Tagen nach dem Einzug in eine neue Wohnung müssen Sie Ihre Adresse beim örtlichen Bürgeramt anmelden. Sie benötigen einen Reisepass, ein ausgefülltes Anmeldeformular und eine Wohnungsgeberbestätigung des Vermieters.',
                    content_ru='В течение 14 дней после переезда в новое жилье вы должны зарегистрировать свой адрес в местном Bürgeramt. Вам понадобятся паспорт, заполненная форма регистрации и подтверждение от арендодателя (Wohnungsgeberbestätigung).'
                ),
                WikiItem(
                    title_uz='Germaniyada tibbiy sug\'urta',
                    title_de='Krankenversicherung in Deutschland',
                    title_ru='Медицинское страхование в Германии',
                    category_id=cat_insurance.id,
                    content_uz='Germaniyada tibbiy sug\'urta majburiydir. Siz davlat sug\'urtasi (Gesetzliche Krankenversicherung - GKV), masalan TK, AOK, Barmer, yoki agar daromad talablariga javob bersangiz, xususiy sug\'urta (Private Krankenversicherung - PKV) ni tanlashingiz mumkin.',
                    content_de='Die Krankenversicherung ist in Deutschland obligatorisch. Sie können zwischen einer gesetzlichen Krankenversicherung (GKV) wie TK, AOK, Barmer oder einer privaten Krankenversicherung (PKV) wählen, wenn Sie die Einkommensgrenzen überschreiten.',
                    content_ru='Медицинское страхование обязательно в Германии. Вы можете выбрать государственное страхование (Gesetzliche Krankenversicherung - GKV), такое как TK, AOK, Barmer, или частное (Private Krankenversicherung - PKV), если вы соответствуете требованиям по доходу.'
                )
            ]
            db.session.add_all(wiki)

        # Seed Services
        if not Service.query.first():
            print("Seeding Services...")
            services = [
                Service(
                    name='Dilshod Turdiev',
                    role='Certified Sworn Translator (Uzbek-German-Russian)',
                    city='Frankfurt',
                    verified=True,
                    category='Translations',
                    contact='@dilshod_translator'
                ),
                Service(
                    name='Anvar Khusanov',
                    role='Legal Consultant (Immigration & Business Law)',
                    city='Berlin',
                    verified=True,
                    category='Legal Support',
                    contact='@anvar_consulting'
                ),
                Service(
                    name='Uzbek Academic Association Germany e.V.',
                    role='Community Union & Student Support Organization',
                    city='Munich',
                    verified=True,
                    category='Community Unions',
                    contact='@uz_academic_germany'
                )
            ]
            db.session.add_all(services)

        db.session.commit()
        print("Database Seeded Successfully!")

if __name__ == '__main__':
    seed_database()
