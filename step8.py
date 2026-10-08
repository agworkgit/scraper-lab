import pandas as pd
import streamlit as st

fruit = pd.DataFrame({"name": ["apple", "pear", "plum"], "price": [0.5, 0.7, 0.3]})

st.title("Fruit prices")
st.metric("Average price", f"£{fruit['price'].mean():.2f}")
st.dataframe(fruit)
st.bar_chart(fruit.set_index("name")["price"])

# for dashboard -> run with streamlit run <file>
