from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()
    phone_number = State()
    work = State()
    past_work = State()     # Oldin qayerlarda ishlagansiz?
    specialty = State()     # Mutaxassisligingiz qanday?
    experience = State()    # Tajriba yilingiz qancha?
    leadership = State()
    reasons = State()      # 3 ta sabab
    problem_solving = State() # Muammoli vaziyatda yo'l tutish
    achievements = State() # Yutuqlar (sertifikat, diplom)
    why_ilmkon = State()   # Nima uchun Ilmkon School?
    extra_comments = State()