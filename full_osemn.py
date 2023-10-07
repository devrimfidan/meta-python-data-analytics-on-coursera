#!/usr/bin/env python
# coding: utf-8

# # Activity: Full OSEMN

# ## Introduction
# 
# In this assignment, you will work on a data analysis project. This project will
# let you practice the skills you have learned in this course and write real code
# in Python.
# 
# You will perform the following steps of the OSEMN framework:  
# - [Scrub](#scrub)
# - [Explore](#explore)
# - [Interpret](#interpret)

# In[ ]:


# We'll import the libraries you'll likely use for this activity
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data
df = pd.read_csv('transactions-pet_store.csv')
df_orig = df.copy()


# ## Scrub
# 
# You will scrub the data. It's important that you follow the directions as
# stated. Doing more or less than what is asked might lead to not getting full
# points for the question.
# 
# ------
# 
# If while you're working on the scrubbing phase you need to reset the DataFrame,
# you can restart the kernel (in the toolbar: "Kernel" > "Restart").

# #### Question 1
# 
# Remove all rows that have are missing either the `Product_Name` or the
# `Product_Category`. Assign the cleaned DataFrame to the variable `df`
# (overwriting the original DataFrame.).

# In[ ]:


# Your code here
# Remove rows with missing values in 'Product_Name' or 'Product_Category'
df = df.dropna(subset=['Product_Name', 'Product_Category'])

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)


# In[ ]:


# Question 1 Grading Checks

assert df.shape[0] <= 2874, 'Did you remove all the rows with missing values for the columns Product_Name & Product_Category?'
assert df.shape[0] >= 2700, 'Did you remove too many the rows with missing values?'
assert len(df.columns) == 10, 'Make sure you do not drop any columns.'


# #### Question 2
# 
# Find any clearly "incorrect" values in the `Price` column and "clean" the
# DataFrame to address those values.
# 
# Ensure you make the changes to the DataFrame assigned to the variable `df`.

# In[ ]:


# Your code here

# Remove very small values
threshold_small = 0.01
df = df[df['Price'] >= threshold_small]

# Remove very large values
threshold_large = 1000
df = df[df['Price'] <= threshold_large]

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)


# In[ ]:


# Question 2 Grading Checks

assert (df.Price < df.Price.quantile(0.0001)).sum() == 0, 'Check for very small values'
assert (df.Price > df.Price.quantile(0.999)).sum() == 0, 'Check for very large values'


# #### Question 3
# 
# After you've done the cleaning above, remove any column that has more than `500`
# missing values.
# 
# Ensure you make the changes to the DataFrame assigned to the variable `df`.

# In[ ]:


# Your code here

# Remove columns with more than 500 missing values
df = df.dropna(axis=1, thresh=df.shape[0] - 500)


# In[ ]:


# Question 3 Grading Checks

assert len(df.columns) < 10, 'You should have dropped 1 or more columns (with more than 500 missing values)'


# #### Question 4
# 
# Address the other missing values. You can replace the values or remvove them,
# but whatever method you decide to clean the DataFrame, you should no longer have
# any missing values.
# 
# Ensure you make the changes to the DataFrame assigned to the variable `df`.

# In[ ]:


# Your code here

# Replace missing values with the mean of each column
df.fillna(df.mean(), inplace=True)

# Check for any remaining missing values in the DataFrame
missing_values = df.isnull().sum().sum()

# Print the number of remaining missing values
print("Number of remaining missing values:", missing_values)


# In[ ]:


# Question 4 Grading Checks

assert df.Customer_ID.isna().sum() == 0, 'Did you address all the missing values?'


# ## Explore
# 
# You will explore the data. It's important that you follow the directions as
# stated. Doing more or less than what is asked might lead to not getting full
# points for the question.
# 
# You may use either exploratory statistics or exploratory visualizations to help
# answer these questions.
# 
# ------
# 
# Note that the DataFrame loaded for this section (in the below cell) is different
# from the data you used in the [Scrub](#scrub) section.
# 
# If while you're working on the scrubbing phase you need to reset the DataFrame,
# you can restart the kernel (in the toolbar: "Kernel" > "Restart").

# In[ ]:


df = pd.read_csv('transactions-pet_store-clean.csv')


# #### Question 5
# 
# Create a `Subtotal` column by multiplying the `Price` and `Quantity` values. 
# This represents how much was spent for a given transaction (row).

# In[ ]:


# Your code here

# Create a Subtotal column
df['Subtotal'] = df['Price'] * df['Quantity']


# In[ ]:


# Question 5 Grading Checks

assert 'Subtotal' in df.columns, ''


# #### Question 6
# 
# Determine most common category (`Product_Category`) purchases (number of total
# items) for both `Product_Line` categories. Assign the (string) name of these
# categories to their respective variables `common_category_cat` & 
# `common_category_dog`.

# In[ ]:


# Your code here
# Calculate the most common category for the 'cat' Product_Line
common_category_cat = df[df['Product_Line'] == 'cat']['Product_Category'].mode().iloc[0]

# Calculate the most common category for the 'dog' Product_Line
common_category_dog = df[df['Product_Line'] == 'dog']['Product_Category'].mode().iloc[0]

# Print the most common categories
print("Most common category for 'Cat' Product Line:", common_category_cat)
print("Most common category for 'Dog' Product Line:", common_category_dog)


# In[ ]:


# Question 6 Grading Checks

assert isinstance(common_category_dog, str), 'Ensure you assign the name of the category (string) to the variable common_category_dog'
assert isinstance(common_category_cat, str), 'Ensure you assign the name of the category (string) to the variable common_category_cat'


# #### Question 7
# 
# Determine which categories (`Product_Category`), by `Product_Line` have the
# ***median*** highest `Price`.
# Assign the (string) name of these categories to their respective variables
# `priciest_category_cat` & `priciest_category_dog`.

# In[ ]:


# Your code here
# Calculate the median highest priced category for the 'cat' Product_Line
priciest_category_cat = df[df['Product_Line'] == 'cat'].groupby('Product_Category')['Price'].median().idxmax()

# Calculate the median highest priced category for the 'dog' Product_Line
priciest_category_dog = df[df['Product_Line'] == 'dog'].groupby('Product_Category')['Price'].median().idxmax()

# Print the median highest priced categories
print("Median highest priced category for 'Cat' Product Line:", priciest_category_cat)
print("Median highest priced category for 'Dog' Product Line:", priciest_category_dog)


# In[ ]:


# Question 7 Grading Checks

assert isinstance(priciest_category_dog, str), 'Ensure you assign the name of the category (string) to the variable priciest_category_dog'
assert isinstance(priciest_category_cat, str), 'Ensure you assign the name of the category (string) to the variable priciest_category_cat'


# ## Modeling
# 
# This is the point of the framework where we'd work on modeling with our data.
# However, in this activity, we're going to move straight to interpretting.

# ## Interpret
# 
# You will interpret the data based on what you found so far. It's important that
# you follow the directions as stated. Doing more or less than what is asked might
# lead to not getting full points for the question.
# 
# 
# ------
# 
# Note that the DataFrame loaded for this section (in the below cell) is the same
# as the data you used in the [Explore](#explore) section.
# 
# If while you're working on the scrubbing phase you need to reset the DataFrame,
# you can restart the kernel (in the toolbar: "Kernel" > "Restart").

# #### Question 8
# 
# You want to emphasize to your stakeholders that the total number of product
# categories sold differ between the two `Product_Line` categories (`'cat'` & 
# `'dog'`).
# 
# Create a **_horizontal_ bar plot** that has `Product_Category` on the y-axis and
# the total number of that category sold (using the `Quantity`) by each 
# `Product_Line` category. Also **change the axis labels** to something meaningful
# and add a title.
# 
# You will likely want to use Seaborn. Make sure you set the result to the
# variable `ax` like the following:
# ```python
# ax = # code to create a bar plot
# ```

# In[ ]:


# Your code here
import seaborn as sns
import matplotlib.pyplot as plt

# Group the DataFrame by 'Product_Line' and 'Product_Category' and sum the quantities
category_quantity = df.groupby(['Product_Line', 'Product_Category'])['Quantity'].sum().reset_index()

# Create a horizontal bar plot
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='Quantity', y='Product_Category', hue='Product_Line', data=category_quantity)

# Set axis labels and title
ax.set_xlabel('Total Quantity Sold')
ax.set_ylabel('Product Category')
ax.set_title('Total Quantity of Product Categories Sold by Product Line')

# Show the plot
plt.show()


# In[ ]:


# Question 8 Grading Checks

assert isinstance(ax, plt.Axes), 'Did you assign the plot result to the variable ax?'


# #### Question 9
# 
# Based on the plot from [Question 8](#question-8), what would you conclude for
# your stakeholders about what products they should sell? What would be the
# considerations and/or caveats you'd communicate to your stakeholders?
# 
# Write at least a couple sentences of your thoughts in a string assigned to the
# variable `answer_to_9`.
# 
# The cell below should look something like this:
# ```python
# answer_to_9 = '''
# I think that based on the visualization that ****.
# Therefore I would communicate with the stakeholders that ****
# '''
# ```

# In[ ]:


# Your code here
answer_to_9 = '''
Based on the plot from Question 8, it's evident that there are variations in the total number of product categories sold between the 'cat' and 'dog' Product_Lines. Specifically, for the 'cat' Product_Line, certain product categories appear to be selling in higher quantities compared to the 'dog' Product_Line. These categories may present an opportunity for increased focus in terms of marketing and inventory management.

However, it's important to communicate some considerations and caveats to the stakeholders. Firstly, the total quantity sold alone may not account for the profitability of each product category. Therefore, further analysis should be conducted to assess the profitability of each category. Additionally, it's essential to consider factors such as market demand, customer preferences, and competition when making decisions about what products to sell or promote. Finally, understanding the seasonality of pet product sales and conducting a comprehensive market analysis would provide a more complete picture for strategic decision-making.
'''


# In[ ]:


# Question 9 Grading Checks

assert isinstance(answer_to_9, str), 'Make sure you create a string for your answer.'


# #### Question 10
# 
# The plot you created for [Question 8](#question-8) is good but could be modified
# to emphasize which products are important for the business.
# 
# Create an explanatory visualization that emphasizes the insight you about the
# product category. This would be a visualization you'd share with the business
# stakeholders.
# 
# Make sure you set the result to the variable `ax` like the following:
# ```python
# ax = # code to create explanatory visualization
# ```

# In[ ]:


# Your code here

import seaborn as sns
import matplotlib.pyplot as plt

# Group the DataFrame by 'Product_Line' and 'Product_Category' and sum the quantities
category_quantity =


# In[ ]:


# Question 10 Grading Checks

assert isinstance(ax, plt.Axes), 'Did you assign the plot result to the variable ax?'

