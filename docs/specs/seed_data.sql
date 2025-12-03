-- ============================
-- Inserts de prueba para demo
-- ============================

-- Trabajadores
INSERT INTO trabajador (id_trabajador, nombre, apellidos, correoelectronico, contrasenya, rol, id_tarjeta)
VALUES
(1, 'Samuel', 'Lopez Suarez', 'samuel.lopezsuarez@demo.com', 'pass123', 'profesor', '43be8f18'),
(2, 'Andrea', 'Rexona Galan', 'andrea.rexonagalan@demo.com', 'pass123', 'personal_servicio', 'e3c78e18');

-- Profesor vinculado al trabajador 1
INSERT INTO profesor (id_profesor) VALUES (1);

-- Personal de servicio vinculado al trabajador 2
INSERT INTO personalservicio (id_personal) VALUES (2);

-- Alumnos
INSERT INTO alumno (id_alumno, nombre, apellidos, correoelectronico, contrasenya, id_tarjeta)
VALUES
(1, 'Rocio', 'Garcia Miranda', 'rocio.garciamiranda@demo.com', 'pass123', 'b339418'),
(2, 'Joan', 'Catalan Fernandez', 'joan.catalanfernandez@demo.com', 'pass123', 'a885522');

-- Asignaturas
INSERT INTO asignatura (id_asignatura, id_profesor, nombre, descripcion)
VALUES
('P1', 1, 'Programacion', 'Asignatura de DAW, DAM y ASIX'),
('Pr3', 1, 'Proyecto', 'Asignatura de DAW, DAM y ASIX'),
('T4', 1, 'Tutoria', 'Asignatura de DAW, DAM y ASIX'),
('S2', 1, 'Sistemas', 'Asignatura de DAW, DAM y ASIX');

-- Horarios de asignaturas
INSERT INTO horario_a (id_horario_a, id_asignatura, dia, hora, aula)
VALUES
(1, 'P1', 'lunes', '15:30', 'Aula 101'),
(2, 'S2', 'lunes', '17:00', 'Aula 101'),
(3, 'Pr3', 'lunes', '18:00', 'Aula 101'),
(4, 'Pr3', 'martes', '17:00', 'Aula 101'),
(5, 'T4', 'martes', '19:00', 'Aula 101'),
(6, 'P1', 'miercoles', '17:00', 'Aula 101'),
(7, 'S2', 'miercoles', '18:00', 'Aula 101'),
(8, 'Pr3', 'jueves', '15:30', 'Aula 101'),
(9, 'P1', 'jueves', '17:00', 'Aula 101'),
(10, 'Pr3', 'viernes', '17:00', 'Aula 101'),
(11, 'S2', 'viernes', '18:00', 'Aula 101');

-- Horario de trabajadores (ejemplo de asistencia)
INSERT INTO horario_t (id_horario_t, id_trabajador, fecha, hora)
VALUES
(1, 2, '2025-12-02', '15:00'),
(2, 1, '2025-12-02', '15:00');

-- Asistencia de alumnos
INSERT INTO asiste (id_alumno, id_asignatura, fecha, hora, asistio)
VALUES
(1, 'Pr3', '2025-12-02', '17:00', TRUE),
(2, 'Pr3', '2025-12-02', '17:00', FALSE);
