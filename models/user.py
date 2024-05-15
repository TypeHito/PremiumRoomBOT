class User:
    def __init__(self, user_id, telegram_id, first_name, enter_name,
                 user_name, is_premium, phone, total_amount, purchase_count,
                 rate, review, referral_id, referrals_count, bot_menu, update_by,
                 init_at, start_at, end_at, premium_status):
        self.user_id = user_id
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.enter_name = enter_name
        self.user_name = user_name
        self.is_premium = is_premium
        self.phone = phone
        self.total_amount = total_amount
        self.purchase_count = purchase_count
        self.rate = rate
        self.review = review
        self.referral_id = referral_id
        self.referrals_count = referrals_count
        self.bot_menu = bot_menu
        self.update_by = update_by
        self.init_at = init_at
        self.start_at = start_at
        self.end_at = end_at
        self.premium_status = premium_status

    def __repr__(self):
        return f"""
user_id: {self.user_id}
telegram_id: {self.telegram_id}
first_name: {self.first_name}
last_name: {self.enter_name}
user_name: {self.user_name}
is_premium: {self.is_premium}
phone: {self.phone}
total_amount: {self.total_amount}
purchase_count: {self.purchase_count}
rate: {self.rate}
review: {self.review}
referral_id: {self.referral_id}
referrals_count: {self.referrals_count}
bot_menu: {self.bot_menu}
update_by: {self.update_by}
init_at: {self.init_at}
start_at: {self.start_at}
end_at: {self.end_at}
premium_status: {self.premium_status}
"""

    def user_status(self):
        return f"""#Info

👤 Ismi:  {self.first_name}
💼 Referral:  {self.referral_id}
👥 Referralar soni:  {self.referrals_count}
🗓 Obuna boshlangan:  {self.start_at}
🗓 Obuna tugash vaqti:  {self.end_at}
⭐️ Obuna xolati:  {self.premium_status}
"""
