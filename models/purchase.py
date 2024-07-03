class Purchase:
    def __init__(self, database, purchase_id, telegram_id, total_amount, status, purchase_at):
        self.database = database
        self.purchase_id = purchase_id
        self.telegram_id = telegram_id
        self.total_amount = total_amount
        self.status = status
        self.purchase_at = purchase_at

