import pandas as pd
def balance_liquid(dataframe):
    # Розрахунок рівномірного розподілу споживання рідини протягом дня
    dataframe["amount"] = pd.to_numeric(dataframe["amount"], downcast="float")
    total_quantity = dataframe['amount'].sum()
    print(f"Загальна кількість рідини: {total_quantity} мл")
    num_periods = 3  # Кількість періодів (ранок, день, вечір)
    quantity_per_period = total_quantity / num_periods

    # Виведення рекомендацій щодо розподілу споживання рідини
    print("Рекомендоване споживання рідини:")
    result = ''
    for period in range(num_periods):
        result += f"{period+1}. {quantity_per_period} мл\n"
    return result