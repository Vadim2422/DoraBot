from bot.utils.unit_of_work import IUnitOfWork


class BaseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
