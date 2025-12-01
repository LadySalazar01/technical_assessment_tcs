# DevOps Technical Assessment TCS – Banco Pichincha

**Autor:** [Lady Geraldine Salazar Bayona]  
**Fecha:** [31 de noviembre del 2025]  

---

## 1️⃣ Resumen del Proyecto
El objetivo de este proyecto fue diseñar, desarrollar, desplegar y monitorear un microservicio que expone un endpoint `/DevOps`.
- Contenerización con Docker  
- Despliegue en Kubernetes con **Minikube**  
- Escalado automático con **HPA**  
- Monitoreo con **Prometheus y Grafana**  
- Exposición segura del endpoint con **APIKey y JWT**  
- Pipeline CI/CD automatizado con **build, test y deploy** 

> ⚠️ **Nota:** La implementación se realizó de manera local utilizando **Minikube** y no se empleó Terraform, por lo que la infraestructura es local. Para exponer el microservicio a Internet se utilizó **ngrok**.

**Endpoint público:**  
[https://epicedial-unmedically-isiah.ngrok-free.dev/DevOps](https://epicedial-unmedically-isiah.ngrok-free.dev/DevOps)  

Para realizar pruebas, es necesario levantar el servicio localmente; pueden comunicarse conmigo para coordinarlo.

---

## 2️⃣ Tecnologías y Lenguaje
- **Lenguaje del microservicio:** Python 3.11  
- **Framework web:** Flask  
- **Dependencias:** `Flask`, `pytest` para pruebas, `requests` para scripts internos  
- **Contenerización:** Docker  
- **Orquestador:** Kubernetes (Minikube)  
- **Pipeline CI/CD:** GitHub Actions (YAML)  
- **Monitoreo:** Prometheus y Grafana  

> Se eligió Python + Flask por su simplicidad para exponer endpoints REST y fácil integración con Docker y pruebas unitarias.

---

## 3️⃣ Infraestructura Local
- **Cluster Kubernetes:** Minikube (1 nodo principal)  
- **Namespaces:**  
  - `devops-ns`: microservicio  
  - `monitoring`: Prometheus y Grafana  
  ### 3.1 Pods en ejecución - Namespace devops-ns
    ![Pods DevOps](img/pods_by_ns.png)
    ### 3.2 Deployments
    ![Deployments](img/number_deployments.png)
    ### 3.3 Servicios expuestos
    ![Services](img/services.png)

    ### 3.4 HPA
    ![HPA](img/hpa.png)

    ### 3.5 Grafana Dashboard
    ![Grafana CPU/Memory](img/grafana_dashboard.png)

**Por qué Minikube:**  
- Entorno local rápido de Kubernetes  
- Permite simular despliegue de pods, HPA, servicios y métricas  
- Compatible con Helm y ngrok  

**Servicios implementados:**  
- Deployment del microservicio `devops-chart` con **2 réplicas**  
- Horizontal Pod Autoscaler: escalar entre 2 y 5 réplicas según CPU  
- Service tipo loadBalancer para comunicación interna  
- Exposición externa mediante ngrok  

**Monitoreo:**  
- Metrics Server para HPA  
- Prometheus para métricas de pods y nodos  
- Grafana para dashboards de CPU, memoria y alertas  

---
## 4️⃣Instalación de dependencias

El microservicio requiere librerías de Python que se encuentran en el archivo [requirements.txt](https://github.com/LadySalazar01/technical_assessment_tcs/blob/main/app/requirements.txt)  . 

### requirements.txt

Contiene todas las dependencias necesarias para ejecutar el microservicio.

### Para instalar las dependencias:

```bash
# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar el entorno virtual
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```
---

## 5️⃣ Generación del JWT
- Se proporciona un script en Python para generar el JWT:
[Script en github](https://github.com/LadySalazar01/technical_assessment_tcs/tree/main/scripts)  
### Cómo Ejecutar el Script de Generación de JWT

### 1. Guardar el script

Guarda el código como `generate_jwt.py` (o `gen_jwt.py`).

### 2. (Opcional) Definir clave secreta para JWT

**Linux/Mac:**
```bash
export JWT_SECRET="dev_secret_for_testing"
```

**Windows PowerShell:**
```powershell
$env:JWT_SECRET="dev_secret_for_testing"
```

**Windows CMD:**
```cmd
set JWT_SECRET=dev_secret_for_testing
```

### 3. Ejecutar el script
```bash
python generate_jwt.py
```

O si tu archivo se llama `gen_jwt.py`:
```bash
python scripts/gen_jwt.py
```

### 4. Usar el token generado

Copia el token que aparece en la salida y úsalo en el header `X-JWT-KWY`:
```bash
TOKEN=$(python scripts/gen_jwt.py)

curl -X POST https://epicedial-unmedically-isiah.ngrok-free.dev/DevOps \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
  }'
```

### Salida Esperada

El script generará un token JWT válido similar a:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxMjM0NTY3OC05MGFiLWNkZWYtZ2hpai1rbG1ub3BxcnN0dXYiLCJpYXQiOjE3MDEyMzQ1NjcsImV4cCI6MTcwMTIzNDYyN30.abcdefghijklmnopqrstuvwxyz1234567890
```
### Pruebas con Postman

![Postman Test Correct](img/test_postman.png)

![Postman Test ERROR](img/test_postman_body.png)
---
## 6️⃣ GitHub Actions y Pipeline

- **Repositorio:** GitHub  
- **Stages:** build, test, deploy  
- **Ramas:**  
  - `master` → deploy automático a producción  
  - Otras ramas → ejecución de pruebas y build  
- **Versionamiento:** soporta despliegue de versiones específicas  
- **Revisión:** automatizada con pruebas unitarias (`pytest`) y verificación de "Clean Code"  

---

## 7️⃣ Monitoreo

- **Prometheus:** recolecta métricas de pods, nodos y HPA  
- **Grafana:** dashboards con métricas de CPU, memoria y alertas configuradas  
- **Metrics Server:** habilitado para Horizontal Pod Autoscaler  

> La instalación de Prometheus y Grafana se realizó mediante Helm en el namespace `monitoring`.

---

## 8️⃣ Observaciones y Recomendaciones

- Infraestructura local, no se utilizó Terraform  
- Exposición temporal mediante ngrok  
- Para pruebas externas, levantar el servicio localmente y comunicarse para generar URL pública  
- Microservicio desarrollado en Python 3 + Flask  
- Seguridad mediante API Key y JWT dinámico  
- Pruebas realizadas con curl y Postman  
- Requiere instalar librerías definidas en `requirements.txt`






