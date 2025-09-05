# EventTracker

Uma biblioteca simples para rastreamento de eventos.
Atualmente integrada com Sentry, mas projetada para ser extensível a outros provedores.

## Instalação

### Como utilizar no teu projeto?
Hoje a biblioteca não está publicada no PyPI e não pretendemos publicar tão cedo.
Por enquanto, você pode fazer referência pelo repositório GitHub:


#### Exemplo utilizando Poetry:
```bash
poetry add git+https://github.com/MaisTodos/EventTracker.git
```


## Configuração Inicial

```python
from event_tracker import EventTracker

# A inicialização só precisa e deve ser feita uma vez, ao inicio da aplicação.
# Funciona como singleton.
EventTracker.init(
    environment="production",
    sentry_dsn="YOUR_SENTRY_DSN",
    sentry_trace_sample_rate=1.0,
)
```

## Uso

É interessante que a aplicação defina enums para os eventos, tags e contextos que serão utilizados.
É uma boa prática para manter o código limpo, mas principalmente de evitar erros de digitação.


### Rastreamento de Erros

```python
from event_tracker import EventTracker


try:
    1 / 0
except ZeroDivisionError as error:
    EventTracker.track(error)
```

### Enviando eventos

```python
from event_tracker import EventTracker

# Enviando evento com Enum
EventTracker.track("user_action")
```

### Enums

```python
from event_tracker import EventTracker
from enum import Enum

class UserEvents(Enum):
    LOGIN = "user_login"
    LOGOUT = "user_logout"
    REGISTRATION = "user_registration"
    PASSWORD_RESET = "user_password_reset"

class UserType(Enum):
    ADMIN = "admin"
    REGULAR = "regular"
    PREMIUM = "premium"

EventTracker.track(UserEvents.LOGIN)
EventTracker.track(UserEvents.LOGIN.value)
```

### Tags

As tags são pares chave-valor simples, geralmente utilizadas para filtrar e indexar eventos.
As chaves precisam ser Enums ou strings, e os valores precisam ser qualquer tipo primitivo(String's, Inteiros, Floats ou Booleanos).


```python
from event_tracker import EventTracker

EventTracker.track(
    UserEvents.LOGIN,
    tags={
        "user_type": UserType.ADMIN,
        "source": "web_app" 
    }
)
```

### Contextos

Os contextos são dados estruturados, geralmente utilizados para fornecer mais detalhes sobre o evento.
Eles são enviados como dicionários aninhados, mas ao final, os valores precisam ser tipos primitivos.


```python
from event_tracker import EventTracker

EventTracker.track(
    UserEvents.LOGIN,
    context={
        "user_info": {
            "id": "12345",
            "email": "usuario@exemplo.com",
            "subscription": UserType.PREMIUM.value
        },
        "session": {
            "ip": "192.168.1.1",
            "user_agent": "Mozilla/5.0...",
            "session_duration": 3600
        },
        "feature_flags": {
            "new_dashboard": True,
            "beta_features": False
        }
    }
)
```


## Configurando Tags e Contextos Globais

É possivel que a aplicação defina tags e contextos que serão enviados em todos os eventos.
É interessante para informações que não mudam com frequência, como versão da aplicação, ambiente, etc.
Um cenário comum é definir informações da requisição atual, como ID do usuário, IP, User-Agent, assim que a requisição é recebida.


```python
EventTracker.set_contexts({
    "app_info": {
        "version": "1.2.3",
        "environment": Environment.PRODUCTION.value,
        "build_number": "456"
    },
    "server": {
        "region": "us-east-1",
        "instance_id": "i-1234567890abcdef0"
    }
})

EventTracker.set_tags({
    "service": "user-service",
    "cloud_provider": "aws",
    "version": "v1.2.3"
})
```


## Contribuindo

TODO: Adicionar instruções de contribuição.

TODO: adicionar como setar tags e releases para publicar o esse pacote python.

