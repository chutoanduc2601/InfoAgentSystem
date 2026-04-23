# Info Agent System

Hệ thống fullstack gồm **Frontend (React)** và **Backend (Spring Boot)** phục vụ cho việc xây dựng các agent xử lý thông tin.

---

## Cấu trúc project

```
info-agent-system/
├── fe/   # Frontend - React (Vite)
├── be/   # Backend - Spring Boot
└── README.md
```

---

## Công nghệ sử dụng

### Frontend

* React (Vite)
* TypeScript

### Backend

* Spring Boot
* Maven

---

## ⚙Cài đặt & chạy project

### 1. Clone project

```bash
git clone https://github.com/chutoanduc2601/InfoAgentSystem.git
cd InfoAgentSystem
```

---

### 2. Chạy Backend (Spring Boot)

```bash
cd be
./mvnw spring-boot:run
```

👉 Server chạy tại:
http://localhost:8080

---

### 3. Chạy Frontend (React)

```bash
cd fe
npm install
npm run dev
```

👉 Frontend chạy tại:
http://localhost:5173

