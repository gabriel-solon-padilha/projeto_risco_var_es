# Gerenciamento_de_risco_var_es

Projeto de finanças em que calculo algumas importantes métricas de gerenciamento de riscos (VAR e ES) a partir dos os retornos de uma série de preços

## Conceitos usados

### Retornos

Seja $P_t$ o preço de um ativo no instante $t$.
O retorno simples é dado por:
$$ retorno_t = \frac{preço_t - preço_{t-HP}}{preço_{t-HP}} $$
ou
$$ retorno_t = \frac{preço_t}{preço_{t-HP}} -1 $$

Geralmente o retorno é expresso em porcentagem, relativamente ao período. Também é chamado de *taxa de retorno*.   
E o PnL é dado por:

$$ PnL_t = preço_t - preço_{t-HP} $$
ou
$$ PnL_t = retorno_t \cdot preço_{t-HP} $$

e representa a perda ou ganho em valor financeiro ocorrida no período decorrido da variação de preços do ativo.

### Var

- Pior perda esperada sob condições normais de mercado, ao longo de determinado intervalo de tempo ($HP$) e dentro de determinado nível de confiança ($1−\alpha$).

Definição:   
Seja $x(t)$ a série temporal de resultados (PnL), então:

$$ VaR_{1-\alpha}^{HP}(t) = \inf \{y \in \mathbb{R}: Pr(x(t)) > y = 1 - \alpha \} $$

Exemplo:   
Se um portfólio possui um VaR para $HP=10$ dias e nível de confiança 95\% no valor de R\$ 1 milhão, significa que:
- Há uma probabilidade de $\alpha = 5\%$ que o portfólio perca mais de R$ 1 milhão num intervalo de 10 dias, caso o portfólio permaneça o mesmo neste período. 

### ES

- Valor esperado (média) da perda condicional ao estouro do VaR, ao longo de determinado intervalo de tempo ($𝐻𝑃$) e dentro de determinado nível de confiança ($1−\alpha$).

Definição:
$$ ES_{1-\alpha}^{HP}(t) = \mathbb{E}[x(t) | x(t) < VaR_{1-\alpha}^{HP}(t)] $$

Exemplo:   
Se o ES é de R\$ 10 milhões, significa que:
- Caso ocorra uma perda pior que o VaR (estouro), o valor esperado dessa perda é de R\$ 10 milhões.
