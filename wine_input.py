#!/usr/bin/env/ python3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols, glm

# Read the data set into a pandas DataFrame
wine = pd.read_csv('winequality-both.csv', sep =',', header=0)
wine.columns = wine.columns.str.replace(' ','_')
print(wine.head())
print(wine.info())

# Display descriptive statistics for all variables
print(wine.describe())

# Identify unique values (유일 값)
print(sorted(wine.quality.unique()))

# Calculate value frequencies
print(wine.quality.value_counts())

# Display descriptive statistics for quality by wine type
print(wine.groupby('type')[['alcohol']].describe().unstack('type'))

# Calculate specific qualities (특정 사분 위수 계산)
print(wine.groupby('type')[['quality']].quantile([0.25, 0.75]).unstack('type'))

# Calculate correlation matrix for all variables
print("================================================wine corr=====================================================")

print(wine.corr())

# 변수간 관계 살펴보기(산점도 작성)
# Look at relationship between pairs of variables
# Take a "small" sample of red and white wines for plotting
def take_sample(data_frame, replace=False, n=200):
	return data_frame.loc[np.random.choice(data_frame.index, replace=replace, size=n)]
reds = wine.loc[wine['type']=='red', :]
whites = wine.loc[wine['type']=='white', :]
reds_sample = take_sample(wine.loc[wine['type']=='red', :])
whites_sample = take_sample(wine.loc[wine['type']=='white', :])
wine_sample = pd.concat([reds_sample, whites_sample])
wine['in_sample'] = np.where(wine.index.isin(wine_sample.index), 1.,0.)

reds_sample = reds.loc[np.random.choice(reds.index, 100)]
whites_sample = whites.loc[np.random.choice(whites.index, 100)]
wine_sample = pd.concat([reds_sample,whites_sample], ignore_index=True)

print(wine['in_sample'])
print(pd.crosstab(wine.in_sample, wine.type, margins=True))

sns.set_style("dark")
# sns.set_style("darkgrid", {"legend.scatterpoints": 0})
# pg = sns.PairGrid(wine_sample, hue="type", hue_order=["red", "white"], palette=dict(red="red", white="white"), hue_kws={"marker": ["o", "s"]}, \
# 	vars=['quality', 'alcohol', 'residual_sugar'])
# pg.x = wine_sample.ix[wine_sample['type']=='red', 'quality']
# pg = pg.map_diag(plt.hist)
# pg.x = wine_sample.ix[wine_sample['type']=='white', 'quality']
# pg = pg.map_diag(plt.hist)
# pg = pg.map_offdiag(plt.scatter, edgecolor="black", s=10, alpha=0.25)
# #plt.show()

g = sns.pairplot(wine_sample, kind='reg', plot_kws={"ci": False, "x_jitter":0.25, "y_jitter":0.25}, \
	hue='type', diag_kind='hist', diag_kws={"bins":10, "alpha":1.0}, palette=dict(red="red", white="white"), \
		markers=["o", "s"], vars=['quality', 'alcohol', 'residual_sugar'])


print(g)
plt.suptitle('Histograms and Scatter Plots of Quality, Alcohol, and Residual Sugar', fontsize=14, horizontalalignment='center', verticalalignment='top', x=0.5, y=0.999)
plt.show()

# Look at the distribution of quality by wine type
red_wine = wine.loc[wine['type']=='red', 'quality']
white_wine = wine.loc[wine['type']=='white', 'quality']

sns.set_style("dark")
print(sns.distplot(red_wine, norm_hist=True, kde=False, color="red", label="Red wine"))
print(sns.distplot(white_wine, norm_hist=True, kde=False, color="white", label="White wine"))
sns.utils.axlabel("Quality Score", "Density")
plt.title("Distribution of Quality by Wine Type")
plt.legend()
plt.show()

# Test whether mean quality is different between red and white wines
print(wine.groupby(['type'])[['quality']].agg(['std', 'mean']))
tstat, pvalue, df = sm.stats.ttest_ind(red_wine, white_wine)
print('tstat: %.3f pvalue: %.4f' % (tstat, pvalue))

my_formula = 'quality ~ alcohol + chlorides + citric_acid + density + fixed_acidity + free_sulfur_dioxide + pH + residual_sugar + sulphates + total_sulfur_dioxide + volatile_acidity'


print("선형회귀 모델 학습 출력 값")
lm = ols(formula = my_formula, data=wine).fit()
'''
이거 data=wine 부분 in_sample이랑 qaulity type 다 들어가있음 why?
근데 아랫부분 표준화 파트 보면 in_sample, quality, type 다 날리고 전체 표준화 작업들어감
그러고 나서 다시 선형 회귀분석 결과값 출력대는
data=wine_standardized 값으로 함.
그러면 위의 출력값이 같을수가 있나?????
'''


# 또는 lm = glm(my_formula, data=wine, family=sm.families.Gaussian()).fit()
print(lm.summary())
print("\nQuantities you can extract from the result:\n%s" %dir(lm))
print("\nCoefficients:\n%s" % lm.params)
print("\nCoefficient Std Errors:\n%s" % lm.bse)
print("\nAdj. R-squared:\n%.ef" % lm.rsquared_adj)
print("\nF-statistic: %.1f P-value: %.2f" % (lm.fvalue, lm.f_pvalue))
print("\nNumber of obs: %d Number of fitted values: %s" % (lm.nobs, len(lm.fittedvalues)))


#와인 데이터셋의 quality를 종속변수로 생성
print("======================================== 독립변수 표준화를 진행한뒤 출력===================================================")
dependent_variable = wine['quality']
independent_variables = wine[wine.columns.difference(['quality', 'type', 'in_sample'])]
print(wine.columns)

# quality와 type과 in_sample을 제외하고 모든컬럼을 넣는다는 의미 

# print(" 표준화 값 비교")
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()

# scaler.fit(independent_variables)

# independent_variables = scaler.transform(independent_variables)

# wine_standardized = scaler.transform(independent_variables)

# print(wine_standardized)

# logit_model = sm.OLS(dependent_variable, wine_standardized).fit()

independent_variables_standardized = (independent_variables - independent_variables.mean()) / independent_variables.std()
wine_standardized = pd.concat([dependent_variable, independent_variables_standardized], axis=1)
print("axis 테스트 \n")
print("종속 변수 출력\n" ,dependent_variable)
print("표준화 된 독립변수 출력\n", independent_variables_standardized)
print("전체 표준화 axis 값 출력\n", wine_standardized)

print("선형 회귀 분석 변수값 테스트")
print(wine.info())
print(wine_standardized)


lm_standardized = ols(my_formula, data=wine_standardized).fit()

print("테스트")
print(lm_standardized)
print(wine_standardized)

print(lm_standardized.summary())

#기존 데이터셋의 처음 10개의 값을 가지고 '새로운' 관측값 데이터셋을 만듬
new_observations = wine.loc[wine.index.isin(range(10)), independent_variables.columns]
y_predicted = lm.predict(new_observations)
y_predicted_rounded = [round(score, 2) for score in y_predicted]

print(y_predicted_rounded)