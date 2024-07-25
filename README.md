# Wizard Academy

Bienvenido a Wizard Academy, una aplicación para gestionar y administrar los registros de magos y sus solicitudes dentro del Reino de Clover. Esta aplicación está diseñada para interactuar con DynamoDB utilizando `aioboto3`, FastApi  y Python 3.10, y está estructurada según los principios de Clean Code y Clean Architecture.

## Características

- **Registro de Magos**: Gestiona la información de los magos incluyendo sus habilidades mágicas y estado.
- **Solicitudes de Magos**: Administra las solicitudes realizadas por los magos, permitiendo actualizaciones y consultas.
- **Actualizaciones Asíncronas**: Utiliza `aioboto3` para realizar operaciones asíncronas con DynamoDB.
- **Agrupación de Registros**: Permite agrupar registros por diferentes atributos y modelar la salida de manera estructurada.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
📦doc # Documentación de la aplicación.
📦src
 ┣ 📂app
 ┃ ┣ 📂api # Controllers de la aplicación.
 ┃ ┣ 📂core # Artefactos como utils, extensions, enums, root class,etc de la aplicación.
 ┃ ┣ 📂models # Dominio de la aplicación.
 ┃ ┣ 📂services # Artefactos de servicio, acceden a al dominio mediante  repositorios de datos.
 ┃ ┣ 📂use_cases # Casos de uso, agrupa funcionalidades asociadas a un caso.
 ┃ ┣ 📜main.py
 ┃ ┗ 
 ┗ 📂tests # Pruebas Unitarias de la aplicación.
 ┃ ┣ 📂e2e
 ┃ ┣ 📂unit
 ┃ ┃ ┣ 📂api
 ┃ ┃ ┣ 📂core
 ┃ ┃ ┣ 📂models
 ┃ ┃ ┣ 📂services
 ┗ ┗ ┗ 📂use_cases
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/amorales-iolab93/clean-code-wizard-academy.git
   cd clean-code-wizard-academy

2. Crea y activa un entorno virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate 

3. Instala las dependencias:
   ```bash
    poetry install

## Configuración
Asegúrate de configurar tus credenciales de AWS y las variables de entorno necesarias para interactuar con DynamoDB. Puedes hacerlo mediante un archivo .env o configurando directamente las variables de entorno en tu sistema.

## Uso

### Ejecución de la Aplicación

Asegúrate de configurar tus credenciales de AWS y las variables de entorno necesarias para interactuar con DynamoDB. Puedes hacerlo mediante un archivo .env o configurando directamente las variables de entorno en tu sistema.

#### Inserta la siguente varibales de entorno, utiliza el siguiente comando:

```bash
    export ENVIRONMENT_NAME="LOCAL"
```

En caso de utilziar servicios de aws: 


```bash
    export AWS_ACCESS_KEY_ID="***************"
    export AWS_SECRET_ACCESS_KEY="***************"
    export AWS_SESSION_TOKEN="***************"
```

#### Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
    cd src/
    uvicorn app.main:app --reload --port 8080
```

#### Para ejecutar la aplicación en docker, utiliza el siguiente comando:

```bash
    docker-compose up --build
```

### Ejecución de pruebas unitarias

```bash
    poetry run pytest ./src/tests
```


## Ednpoints

### La aplicación consta de los siguentes endpoints:

    ```
    http://127.0.0.1:8080/docs#/
    ```


#### Solicitudes

1. GET Requests:
    ```bash
    curl --location 'http://127.0.0.1:8080/api/v1/requests'
    ```

2. POST Register:
    ```bash
    curl --location 'http://127.0.0.1:8080/api/v1/requests' \
    --header 'Content-Type: application/json' \
    --data '{
        "name": "Morgana",
        "last_name": "Le Fay",
        "age": 25,
        "magic_skill": "Darkness"
    }'
    ```

3. PUT Update Request: 

    ```bash
    curl --location --request PUT 'http://127.0.0.1:8080/api/v1/requests/323b5cca-b124-4883-9212-00438cfd78b4' \
    --header 'Content-Type: application/json' \
    --data '{
        "name": "Morgana",
        "last_name": "Le Fay",
        "age": 25,
        "magic_skill": "Light"
    }'
    ```

4. DELETE Remove Request: 

    ```bash
    curl --location --request DELETE 'http://127.0.0.1:8080/api/v1/requests/ff4f5469-fa1b-42d4-bb38-3a6318affdfc'
    ```

5. PATCH Set Status Request: 

    ```bash
    curl --location --request PATCH 'http://127.0.0.1:8080/api/v1/requests/323b5cca-b124-4883-9212-00438cfd78b4/status/approved'
    ```
#### Asignaciones

1. GET Assignments:
    ```bash
    curl --location 'http://127.0.0.1:8080/api/v1/assignments'
    ```


#### Las asignaciones se realizan al cambiar el estado de la solicitud de un mago, para ello se realizó:

1. Se debe definir el catálogo de grimorios:
    ```
    class WizardGrimorieTypes(str, Enum):
        ONE_LEAF = "one-leaf-clover"
        TWO_LEAF = "two-leaf-clover"
        THREE_LEAF = "three-leaf-clover"
        FOUR_LEAF = "four-leaf-clover"
    ```
2. Debemos en base a esos catálogos crear dos grupos de muestras, muestras con los elementos más comunes y otra con los menso comunes
    ```
        samples = 5 # numeor de muestras con mayor frecuencia
        special_samples = 1 # numero de muestras con mennos frecuencia 

        random_clover = [1, 2, 3] * samples + [4] * special_samples
        # obtenemso un arreglo con un total de 16 eventos 
        #random_clover : [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4]
        
        choice = random.choice(random_clover)
        clovers = {
            1: WizardGrimorieTypes.ONE_LEAF,
            2: WizardGrimorieTypes.TWO_LEAF,
            3: WizardGrimorieTypes.THREE_LEAF,
            4: WizardGrimorieTypes.FOUR_LEAF,
        }
        return clovers[choice]
    ```

2. Para calcular la probabilidad de que el grimorio de 4 hojas sea de entre un 5 a 10 %
    **Fórmula de Probabilidad: **
    ```
    Probabilidad = (Número de ocurrencias del evento) / (Número total de eventos)
    ```
    Partiendo de esto es necesario poder tener un mayor número  de eventos para ver de manera más exacta estos resultados para ello se realizó la prueba unitaria 

    ```
    def test_clover_random_assignation_probability_greater_than():
        """
        Ensures that the probability of a grimorie of 4 leaf being signed is between 5 and 10 percent
        """
        request_samples = 100000
        choices_clover = [WizardRequestEntity.get_random_grimorie() for _ in range(request_samples)]
        counter = Counter(choices_clover)
        total_sample = sum(counter.values())

        prob_4_clover = counter.get(WizardGrimorieTypes.FOUR_LEAF, 0) / total_sample

        assert 0.05 <= prob_4_clover <= 0.10, "The probability of FOUR_LEAF is outside the expected range"
    ```
    Dando como resultado:
    ```
        Probabilidad de 1 hojas: 31.29%
        Probabilidad de 2 hojas: 31.08%
        Probabilidad de 3 hojas: 31.45%
        Probabilidad de 4 hojas: 6.18%
    ```


## Autor

**[Alan Jonathan M. Sánchez]**

- [LinkedIn](https://www.linkedin.com/in/ajms-me/)

## Contribución
Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos:

Haz un fork del repositorio.
Crea una nueva rama (git checkout -b feature/nueva-feature).
Realiza tus cambios y haz commit (git commit -am 'Añadir nueva feature').
Sube tu rama (git push origin feature/nueva-feature).
Abre un Pull Request.

## Licencia

MIT License

Copyright (c) 2024 [Alan Jonathan Morles Sánchez]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
