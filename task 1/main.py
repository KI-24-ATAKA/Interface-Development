import re


class Date:
  def __init__(self, dd: int, mm: int, yyyy: int):
    self.dd = dd
    self.mm = mm
    self.yyyy = yyyy

  def __str__(self):
    return f"{self.yyyy:04d}-{self.mm:02d}-{self.dd:02d}"


class Patient:
  def __init__( self, passport: str, name: str, birth_date_str: str, phone: str, temperature_str: str,):
    self.passport = passport
    self.name = name
    parts = birth_date_str.split("-")
    self.birth_date = Date(int(parts[2]), int(parts[1]), int(parts[0]))
    self.phone = phone
    self.temperature = float(temperature_str)


print("Введите:")

regular = [
    r"^\d{2} \d{2}-\d{6}$",
    r"^\S+.*$", 
    r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[01])$",
    r"^(\+\d\(\d{3}\) \d{3}-\d{2}-\d{2}|\d\(\d{3}\) \d{3}-\d{4})$",
    r"^\d{2}\.\d{2}$",
]

input_message = [
    "Паспортные данные (формат ss ss-nnnnnn)",
    "Имя (строка)",
    "Дату рождения (формат yyyy-mm-dd)",
    "Номер телефона (формат +X(XXX) XXX-XX-XX или X(XXX) XXX-XXXX)",
    "Температуру (формат XX.XX)",
]

results = []

for i in range(len(regular)):
  print(input_message[i])
  is_input_correct = False
  while not is_input_correct:
    current_field = input().strip()
    if re.match(regular[i], current_field):
      results.append(current_field)
      is_input_correct = True
    else:
      print("Неверный формат ввода, введите данные заново")

patient = Patient(results[0], results[1], results[2], results[3], results[4])

print("")
print("✅ Данные о пациенте успешно сохранены:")
print(f"• Паспорт:        {patient.passport}")
print(f"• ФИО:            {patient.name}")
print(f"• Дата рождения:  {patient.birth_date}")
print(f"• Телефон:        {patient.phone}")
print(f"• Температура:    {patient.temperature:.2f}")