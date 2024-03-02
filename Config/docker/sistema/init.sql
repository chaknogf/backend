
CREATE DATABASE test_api;
GO


USE test_api;
GO


CREATE TABLE `pacientes` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `expediente` int UNIQUE DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `dpi` bigint DEFAULT NULL,
  `pasaporte` varchar(50) DEFAULT NULL,
  `sexo` varchar(2) DEFAULT NULL,
  `nacimiento` date DEFAULT NULL,
  `nacionalidad` int DEFAULT NULL,
  `lugar_nacimiento` int DEFAULT NULL,
  `estado_civil` int DEFAULT NULL,
  `educacion` int DEFAULT NULL,
  `pueblo` int DEFAULT NULL,
  `idioma` int DEFAULT NULL,
  `ocupacion` varchar(50) DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `padre` varchar(50) DEFAULT NULL,
  `madre` varchar(50) DEFAULT NULL,
  `responsable` varchar(50) DEFAULT NULL,
  `parentesco` int DEFAULT NULL,
  `dpi_responsable` bigint DEFAULT NULL,
  `telefono_responsable` int DEFAULT NULL,
  `estado` varchar(2) DEFAULT NULL,
  `exp_madre` int DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `fechaDefuncion` varchar(10) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `expediente_unico` (`expediente`)
) ENGINE=InnoDB CHARSET=utf8mb4;
GO



CREATE TABLE `citas` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `fecha` DATE,
  `expediente` INT,
  `especialidad` INT,
  `cirugia_programada` DATE,
  `nota` VARCHAR(255),
  `estado` BOOLEAN DEFAULT FALSE,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (expediente) REFERENCES pacientes (expediente)
)  ENGINE=InnoDB CHARSET=utf8mb4;
GO



CREATE TABLE `consultas`(
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `hoja_emergencia` VARCHAR(15) UNIQUE,
    `expediente` INT DEFAULT NULL,
    `fecha_consulta` DATE DEFAULT NULL,
    `hora` TIME DEFAULT NULL,
    `nombres` VARCHAR(50) DEFAULT NULL,
    `apellidos` VARCHAR(50) DEFAULT NULL,
    `nacimiento` DATE DEFAULT NULL,
    `edad` VARCHAR(25) DEFAULT NULL,
    `sexo` VARCHAR(1) DEFAULT NULL,
    `dpi` VARCHAR(20) DEFAULT NULL,
    `direccion` VARCHAR(100) DEFAULT NULL,
    `acompa` VARCHAR(50) DEFAULT NULL,
    `parente` INT DEFAULT NULL,
    `telefono` INT DEFAULT NULL,
    `nota` VARCHAR(200) DEFAULT NULL,
    `especialidad` INT DEFAULT NULL,
    `servicio`INT DEFAULT NULL,
    `recepcion` BOOLEAN DEFAULT FALSE,
    `fecha_egreso` DATE DEFAULT NULL,
    `fecha_recepcion`DATETIME DEFAULT NULL,
    `tipo_consulta` INT DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (expediente) REFERENCES pacientes (expediente)
)   ENGINE=InnoDB CHARSET=utf8mb4;
GO


CREATE VIEW `vista_emergencia` AS SELECT id, tipo_consulta, hoja_emergencia, expediente, nombres, apellidos, fecha_consulta, nacimiento, recepcion, fecha_recepcion  FROM consultas;
GO

CREATE VIEW `vista_coex` AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, recepcion, fecha_recepcion  FROM consultas;
GO

CREATE VIEW `vista_ingreso` AS SELECT id, tipo_consulta, expediente, nombres, apellidos, fecha_consulta, nacimiento, especialidad, fecha_egreso, recepcion, fecha_recepcion  FROM consultas;
GO

CREATE VIEW `vista_paciente` AS SELECT id, nombre, apellido, expediente, nacimiento, dpi, sexo, estado  FROM pacientes;
GO

CREATE VIEW `vista_citas` AS SELECT ROW_NUMBER() OVER () AS id, especialidad, DATE_FORMAT(fecha, '%Y-%m-%d') AS dia, COUNT(*) AS total_citas FROM citas WHERE estado = false GROUP BY especialidad, dia;
GO

