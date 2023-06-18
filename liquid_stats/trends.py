import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def create_trend(dataframe):
    # Завантаження даних
    df = dataframe
    # Перетворення стовпця 'date' на тип дати
    df['consumed_date'] = pd.to_datetime(df['consumed_date'])
    df["amount"] = pd.to_numeric(df["amount"], downcast="float")
    # Додавання стовпця 'hour' для представлення години з дати
    df['hour'] = df['consumed_date'].dt.hour

    # Групування за годинами і обчислення середньої кількості рідини
    print(df['hour'])
    hourly_consumption = df.groupby('hour')['amount'].mean()

    print(hourly_consumption)

    # Візуалізація годинного споживання рідини
    fig = plt.figure(figsize=(10, 6))
    plt.plot(hourly_consumption.index, hourly_consumption.values)
    plt.xlabel('Година дня')
    plt.ylabel('Середня кількість')
    plt.title('Динаміка погодинного споживання')
    fig.canvas.draw()
    buf = BytesIO()
    conv = Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
    conv.save(buf, format='PNG')
    buf.seek(0)
    return buf