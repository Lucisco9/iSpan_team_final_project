import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/lucy/BDSE30MP/weather_clean/weather_no_null.csv')
df.info()

columns_of_interest = ['RH', 'Precp']
data_of_interest = df[columns_of_interest]
correlation_matrix = data_of_interest.corr()

print(correlation_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()


sns.pairplot(data_of_interest)
plt.show()
