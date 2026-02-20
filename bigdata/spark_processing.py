import os
os.environ["HADOOP_HOME"] = "C:\\hadoop"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Secure Log Analysis") \
    .getOrCreate()

df = spark.read.csv("data/decrypted_logs.csv", header=True, inferSchema=True)

print("Total log entries:", df.count())

print("Schema:")
df.printSchema()

print("Sample logs:")
df.show(5)

suspicious = df.filter(df.label == "attack")

count = suspicious.count()
print("Suspicious entries:", count)

# Convert Spark DataFrame → Pandas DataFrame
suspicious_pd = suspicious.toPandas()

# Save using pandas (NOT Spark)
output_path = "data/suspicious_logs.csv"
suspicious_pd.to_csv(output_path, index=False)

print("Suspicious logs saved successfully at:", output_path)
