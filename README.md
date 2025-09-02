# EventTracker

Uma biblioteca simples e elegante para rastreamento de eventos usando Sentry com suporte nativo a Enums.

## Características

- ✅ Suporte nativo a Enums para type safety
- ✅ Rastreamento de eventos com contexto rico
- ✅ Sistema de tags para filtragem e indexação
- ✅ Tratamento de exceções integrado
- ✅ Níveis de severidade configuráveis
- ✅ Interface limpa e intuitiva

## Instalação

TODO descobrir como provisionar a lib


## Configuração Inicial

```python
from event_tracker import EventTracker

# Inicialização do EventTracker (uma vez na aplicação)
EventTracker.init_sentry(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment="production"
)

# Agora você pode usar em qualquer lugar sem importar nada mais!
```

## Uso Básico

### Definindo Enums (Recomendado)

```python
from enum import Enum
from event_tracker import EventTracker

class UserEvents(Enum):
    LOGIN = "user_login"
    LOGOUT = "user_logout"
    REGISTRATION = "user_registration"
    PASSWORD_RESET = "password_reset"

class UserType(Enum):
    ADMIN = "admin"
    REGULAR = "regular"
    PREMIUM = "premium"

class Environment(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
```

### Rastreamento Simples de Eventos

```python
# Evento simples usando enum (interface limpa!)
EventTracker.track(UserEvents.LOGIN)

# Evento com string (menos recomendado)
EventTracker.track("user_action")

```

### Rastreamento com Tags

```python
# Interface limpa - sem necessidade de instanciar!
EventTracker.track(
    UserEvents.LOGIN,
    tags={
        UserType.REGULAR: "João Silva",
        Environment.PRODUCTION: "web"
    }
)

# Tags mistas
EventTracker.track(
    UserEvents.REGISTRATION,
    tags={
        "user_id": "12345",
        UserType.PREMIUM: "email",
        Environment.STAGING: "mobile_app"
    }
)
```

### Rastreamento com Contexto Rico

```python
# Interface estática mantém o código limpo
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

### Rastreamento de Erros

```python
try:
    # Alguma operação que pode falhar
    resultado = operacao_complexa()
except Exception as e:
    EventTracker.track(
        UserEvents.LOGIN,
        tags={
            "error_type": type(e).__name__,
            Environment.PRODUCTION: "api"
        },
        context={
            "error_details": {
                "message": str(e),
                "user_id": "12345"
            }
        },
        level="error",
        error=e
    )
```

## Exemplos Avançados

### Sistema de E-commerce

```python
class EcommerceEvents(Enum):
    PRODUCT_VIEW = "product_view"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"
    CHECKOUT_START = "checkout_start"
    PAYMENT_FAILED = "payment_failed"

class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    PIX = "pix"
    BOLETO = "boleto"

# Rastreando visualização de produto
EventTracker.track(
    EcommerceEvents.PRODUCT_VIEW,
    tags={
        ProductCategory.ELECTRONICS: "smartphone",
        "user_segment": "premium"
    },
    context={
        "product": {
            "id": "PROD-12345",
            "name": "iPhone 15",
            "price": 4999.99,
            "category": ProductCategory.ELECTRONICS.value
        },
        "user": {
            "id": "USER-789",
            "tier": "gold"
        }
    }
)

# Rastreando compra
EventTracker.track(
    EcommerceEvents.PURCHASE,
    tags={
        PaymentMethod.PIX: "completed",
        "revenue_tier": "high_value"
    },
    context={
        "transaction": {
            "id": "TXN-456789",
            "amount": 4999.99,
            "currency": "BRL",
            "items_count": 1
        }
    },
    level="info"
)
```

### Monitoramento de Performance

```python
class PerformanceEvents(Enum):
    PAGE_LOAD = "page_load"
    API_CALL = "api_call"
    DATABASE_QUERY = "database_query"

class PerformanceLevel(Enum):
    FAST = "fast"
    NORMAL = "normal"
    SLOW = "slow"

# Monitorando performance de API
import time

start_time = time.time()
try:
    response = api_call()
    duration = time.time() - start_time
    
    performance_level = (
        PerformanceLevel.FAST if duration < 0.5 
        else PerformanceLevel.NORMAL if duration < 2.0 
        else PerformanceLevel.SLOW
    )
    
    EventTracker.track(
        PerformanceEvents.API_CALL,
        tags={
            "endpoint": "/api/users",
            performance_level: str(duration)
        },
        context={
            "performance": {
                "duration_ms": duration * 1000,
                "status_code": response.status_code,
                "response_size": len(response.content)
            }
        },
        level="warning" if duration > 2.0 else "info"
    )
    
except Exception as e:
    EventTracker.track(
        PerformanceEvents.API_CALL,
        tags={
            "endpoint": "/api/users",
            "status": "failed"
        },
        error=e,
        level="error"
    )
```

## Configurando Tags e Contextos Globais

```python
# Interface estática para configurações globais
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

# Definindo tags globais
EventTracker.set_tags({
    "service": "user-service",
    Environment.PRODUCTION: "aws",
    "version": "v1.2.3"
})
```

## Padrões de Uso na Aplicação

### Inicialização no Startup da Aplicação

```python
# main.py ou app.py
from event_tracker import EventTracker
from enum import Enum
import os

class AppEnvironment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

def initialize_tracking():
    """Inicializa o sistema de tracking na aplicação"""
    dsn = os.getenv('SENTRY_DSN')
    environment = os.getenv('ENVIRONMENT', 'development')
    
    # Inicializa uma única vez
    EventTracker.init_sentry(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=1.0 if environment == 'development' else 0.1,
        profiles_sample_rate=1.0 if environment == 'development' else 0.1,
        release=os.getenv('APP_VERSION', '1.0.0')
    )
    
    # Configurar contextos globais
    EventTracker.set_contexts({
        "app": {
            "name": "minha-aplicacao",
            "version": os.getenv('APP_VERSION', '1.0.0')
        }
    })

# Na inicialização da app
if __name__ == "__main__":
    initialize_tracking()
    # resto da aplicação...
```

### Uso em Serviços/Classes

```python
# services/user_service.py
from event_tracker import EventTracker  # Só isso!
from enum import Enum

class UserServiceEvents(Enum):
    USER_CREATED = "user_service_user_created"
    USER_UPDATED = "user_service_user_updated"
    USER_DELETED = "user_service_user_deleted"

class UserService:
    # Não precisa de __init__ para o tracker!
    
    def create_user(self, user_data):
        try:
            # Lógica de criação
            user = self._create_user_in_db(user_data)
            
            # Interface super limpa
            EventTracker.track(
                UserServiceEvents.USER_CREATED,
                tags={
                    "user_type": user_data.get("type", "regular"),
                    "source": "api"
                },
                context={
                    "user": {
                        "id": user.id,
                        "email": user.email
                    }
                }
            )
            
            return user
            
        except Exception as e:
            EventTracker.track(
                UserServiceEvents.USER_CREATED,
                tags={"status": "failed"},
                context={"error_context": user_data},
                error=e,
                level="error"
            )
            raise

# Para uso avançado, você ainda pode acessar a instância
class AdvancedService:
    def __init__(self):
        # Só quando realmente precisar de acesso direto
        self.tracker_instance = EventTracker.get_instance()
```

## Boas Práticas

### ✅ Recomendado

```python
# Inicialize uma vez na aplicação
EventTracker.init_sentry(dsn="YOUR_SENTRY_DSN")

# Use a interface estática em qualquer lugar - DX incrível!
EventTracker.track(Events.USER_LOGIN)

# Use Enums para type safety e padronização
class Events(Enum):
    USER_LOGIN = "user_login"

# Agrupe eventos relacionados em Enums
class AuthEvents(Enum):
    LOGIN = "auth_login"
    LOGOUT = "auth_logout"
    REFRESH_TOKEN = "auth_refresh"

# Use contextos estruturados
EventTracker.track(
    AuthEvents.LOGIN,
    context={
        "user": {"id": "123", "tier": "premium"},
        "session": {"duration": 300}
    }
)
```

### ❌ Evite

```python
# Evite múltiplas inicializações
EventTracker.init_sentry(dsn="dsn1")  # Primeira inicialização
EventTracker.init_sentry(dsn="dsn2")  # Será ignorada (singleton)

# Evite usar sem inicializar
EventTracker.track("evento")  # Vai dar erro com mensagem clara

# Evite strings hardcoded
EventTracker.track("some_random_event")  # Propenso a erros

# Evite contextos não estruturados
context = {"random_data": "mixed_information"}  # Difícil de analisar
```

## API Reference

### `EventTracker.init_sentry(dsn, **sentry_options)`

Inicializa o singleton interno do EventTracker com configurações do Sentry.

**Parâmetros:**
- `dsn` (str): DSN do projeto Sentry
- `**sentry_options`: Opções adicionais para o Sentry (traces_sample_rate, environment, etc.)

**Retorna:**
- `EventTrackerCore`: Instância interna para uso avançado (opcional)

### `EventTracker.track()`

Método principal para rastreamento de eventos (interface estática).

**Parâmetros:**
- `event` (str | Enum): Nome do evento
- `tags` (Dict[str | Enum, Any], optional): Tags para filtragem
- `context` (Dict[str, Any], optional): Dados de contexto detalhados
- `level` (str, optional): Nível de severidade ('info', 'warning', 'error')
- `error` (Exception, optional): Exceção associada

### `EventTracker.set_contexts()`

Define contextos globais da aplicação (interface estática).

### `EventTracker.set_tags()`

Define tags globais para todos os eventos (interface estática).

