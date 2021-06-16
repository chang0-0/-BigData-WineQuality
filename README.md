# -BigData-WineQuality


# Linear Regression (선형 회귀 분석)


<p> 회귀계수(Coefficients) </p>

---
<p>Coefficients:</p>
<p>　　　　　　　  Estimate   　　　　　          P(>|t|)  </p>            
<p> (Intercept) 　　   -17.5791        　　　　          　　  0.012   </p>  
<p> speed   　　　   3.9324      　　　　           　　　0.000   </p> 

---

<span> Coef는 데이터로부터 얻은 계수의 추정치를 말한다. </span>

절편(Intercept)의 추정치는 -17.5791로, speed가 0일 때 dist의 값이다.
speed의 계수 추정치는 3.9324로 speed가 1 증가할 때마다 dist가 3.9324 증가한다는 것을 의미한다.

이를 수식으로 정리하면 아래와 같다.
dist = − 17.5791 + 3.9324 × speed

추정치의 표 중간의 P(>|t|)는 모집단에서 계수가 0일 때, 현재와 같은 크기의 표본에서 이러한 계수가 추정될 확률인 p값을 나타낸다. 이 확률이 매우 작다는 것은, 모집단에서 speed의 계수가 정확히 3.9324는 아니더라도 현재의 표본과 비슷하게 0보다 큰 어떤 범위에 있을 가능성이 높다는 것을 의미한다. 보통 5%와 같은 유의수준을 정하여 p값이 그보다 작으면(p < 0.05), "통계적으로 유의미하다"라고 한다.

즉, speed가 증가할 때 기대되는 dist의 변화는 유의수준 5%에서 통계적으로 유의미하다.

@@결론은 회귀계수를 찾는 과정이 회귀분석이됨


선형 회귀 모델
E(Y) = f(x) = beta0 + beta1X1

</span>

## 코드 해석 의문점 선형회귀분석.

선형회귀분석 결과값 출력하는 summary 부분에서. 표준화값이랑 표준화하지 않은 갑을 추가해서 결과를 비교하는데.
my_formula 를 똑같이 사용하는데
이거 data=wine 부분 in_sample이랑 qaulity type 다 들어가있음 why?
근데 아랫부분 표준화 파트 보면 in_sample, quality, type 다 날리고 전체 표준화 작업들어감
그러고 나서 다시 선형 회귀분석 결과값 출력대는
data=wine_standardized 값으로 함.



















