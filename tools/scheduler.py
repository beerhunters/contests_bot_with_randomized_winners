from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Создаем глобальный планировщик
scheduler = AsyncIOScheduler()

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
#
# # Настройка SQLAlchemy JobStore
# jobstores = {
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')  # Используем SQLite
# }
#
# scheduler = AsyncIOScheduler(jobstores=jobstores)
# scheduler.start()
