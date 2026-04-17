# Documentação do Schema GraphQL

---

## 1. **Estrutura Geral do Schema**

### **ENUMs**
```graphql
enum StatusEmail {
  PENDING
  DONE
  ERROR
  REJECTED
}

enum SendType {
  REGISTER
  PASSWORD_CHANGE
  TWO_FACTOR_AUTH
  PASSWORD_RESET
}

enum ExpirationTime {
  TEN_MINUTES
  FIFTEEN_MINUTES
  TWENTY_MINUTES
  ONE_HOUR
}
```

---

### **Scalars**
```graphql
"""
Scalar customizado para representar data e hora no formato ISO 8601.
Exemplo: 2026-04-16T14:30:00Z
"""
scalar DateTime
```

---

### **Tipos Principais**
```graphql
type EmailNotification {
  idEmail: String!
  recipientEmail: String!
  status: StatusEmail!
  sendType: SendType
  providerResponse: String
  actionLink: String
  code: String
  token: String
  expiresAt: DateTime
  createdAt: DateTime!
  processedAt: DateTime
  updatedAt: DateTime
  rejectionReason: String
  rejectedAt: DateTime
}

type EmailNotificationList {
  items: [EmailNotification!]!
  total: Int!
  page: Int!
  limit: Int!
  hasNextPage: Boolean!
}

type ApiError {
  errorName: String!
  typeError: String!
  statusCode: Int!
}

type ApiResponse {
  success: Boolean!
  data: EmailNotificationResult
  error: ApiError
  message: String
  timestamp: DateTime!
}
```

---

### **Input Types**
```graphql
input EmailNotificationInput {
  recipientEmail: String!
  sendType: SendType!
  actionLink: String
  code: String
  token: String
  expiresAt: ExpirationTime
}

input PaginationInput {
  page: Int! = 1
  limit: Int! = 10
}

input DateRangeInput {
  startDate: DateTime!
  endDate: DateTime!
}
```

---

### **Unions**
```graphql
union EmailNotificationResult = EmailNotification | EmailNotificationList | Boolean
```

---

## 2. **Consultas e Mutations**

### **Queries**
```graphql
type Query {
  emailNotifications(pagination: PaginationInput): ApiResponse!
  emailNotificationById(idEmail: String!): ApiResponse!
  emailNotificationsByStatus(
    status: StatusEmail!,
    pagination: PaginationInput
  ): ApiResponse!
  emailNotificationsByDateRange(
    dateRange: DateRangeInput!,
    pagination: PaginationInput
  ): ApiResponse!
  emailNotificationsCreatedAfter(date: DateTime!, pagination: PaginationInput): ApiResponse!
}
```

---

### **Mutations**
```graphql
type Mutation {
  createEmailNotification(input: EmailNotificationInput!): ApiResponse!
  updateEmailNotification(
    idEmail: String!,
    input: EmailNotificationInput!
  ): ApiResponse!
  deleteEmailNotification(idEmail: String!): ApiResponse!
  deleteAllEmailNotifications: ApiResponse!
  rejectEmailNotification(
    idEmail: String!,
    reason: String
  ): ApiResponse!
  markAsProcessed(idEmail: String!): ApiResponse!
  cleanupOldNotifications(beforeDate: DateTime!): ApiResponse!
}
```

---

### **Subscriptions (Opcionais)**
```graphql
type Subscription {
  emailNotificationStatusChanged(idEmail: String!): EmailNotification!
  emailNotificationCreated: EmailNotification!
  emailNotificationProcessed: EmailNotification!
}
```

---

## 3. **Conceitos Importantes**

### **Paginação**
- **Campos**:
  - `page`: Número da página atual.
  - `limit`: Número de itens por página.
  - `hasNextPage`: Indica se existem mais páginas.
- **Fórmula**:
  ```python
  has_next_page = (page * limit) < total
  ```

- **Exemplo**:
  ```graphql
  query {
    emailNotifications(pagination: { page: 1, limit: 10 }) {
      success
      data {
        ... on EmailNotificationList {
          items {
            idEmail
            recipientEmail
            status
          }
          total
          hasNextPage
        }
      }
      timestamp
    }
  }
  ```

---

### **Campo `reason`**
- Usado como um **motivo opcional** em `rejectEmailNotification`.
- Exemplo:
  ```graphql
  mutation {
    rejectEmailNotification(
      idEmail: "email-123",
      reason: "Email inválido ou expirado"
    ) {
      success
      message
      timestamp
    }
  }
  ```

---

### **Scalar `DateTime`**
- Customizado para trabalhar com datas em formato ISO 8601.
- Exemplo de definição:
  ```graphql
  scalar DateTime
  ```
- Implementação Python:
  ```python
  from datetime import datetime
  from graphene import Scalar
  from graphql.language import ast

  class DateTime(Scalar):
      @staticmethod
      def serialize(dt):
          return dt.isoformat() + "Z" if dt.tzinfo is None else dt.isoformat()

      @staticmethod
      def parse_literal(node):
          if isinstance(node, ast.StringValue):
              return datetime.fromisoformat(node.value.replace("Z", "+00:00"))

      @staticmethod
      def parse_value(value):
          return datetime.fromisoformat(value.replace("Z", "+00:00"))
  ```

---

## 4. **Exemplo Completo**

### Consulta com Paginação
```graphql
query {
  emailNotifications(pagination: { page: 1, limit: 10 }) {
    success
    data {
      ... on EmailNotificationList {
        items {
          idEmail
          recipientEmail
          status
        }
        total
        hasNextPage
      }
    }
    timestamp
  }
}
```

### Rejeitar Notificação
```graphql
mutation {
  rejectEmailNotification(
    idEmail: "email-789",
    reason: "Limite de tentativas excedido"
  ) {
    success
    message
    timestamp
  }
}
```

### Rejeitar sem motivo
```graphql
mutation {
  rejectEmailNotification(idEmail: "email-456") {
    success
    message
  }
}
```