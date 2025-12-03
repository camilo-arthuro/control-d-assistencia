-- ============================
-- Inserts de prueba para demo
-- ============================

-- Trabajadores
INSERT INTO trabajador (nombre, apellidos, correoelectronico, contrasenya, rol, id_tarjeta)
VALUES
('Samuel', 'Lopez Suarez', 'samuel.lopezsuarez@demo.com', 'pass123', 'profesor', '43be8f18'),
('Andrea', 'Rexona Galan', 'andrea.rexonagalan@demo.com', 'pass123', 'personal_servicio', 'e3c78e18');

-- Profesor vinculado al primer trabajador (id_trabajador = 1)
INSERT INTO profesor (id_profesor) VALUES (1);

-- Personal de servicio vinculado al segundo trabajador (id_trabajador = 2)
INSERT INTO personalservicio (id_personal) VALUES (2);

-- Alumnos
INSERT INTO alumno (nombre, apellidos, correoelectronico, contrasenya, id_tarjeta)
VALUES
('Rocio', 'Garcia Miranda', 'rocio.garciamiranda@demo.com', 'pass123', 'b339418'),
('Joan', 'Catalan Fernandez', 'joan.catalanfernandez@demo.com', 'pass123', 'a885522'),
('Carlos', 'Galan Delgado', 'carlos.galan@demo.com', 'pass123', 'c4f9217'),
('Hanna', 'Zipa', 'hanna.zipa@demo.com', 'pass123', 'd7a8429'),
('Harold', 'Warnes', 'harold.warnes@demo.com', 'pass123', 'e9b1534'),
('Ruben', 'Martinez Caballero', 'ruben.martinez@demo.com', 'pass123', 'f2c6718'),
('Juan', 'Flores Rodriguez', 'juan.flores@demo.com', 'pass123', 'a1d9823');

-- Asignaturas (profesor con id 1)
INSERT INTO asignatura (id_asignatura, id_profesor, nombre, descripcion)
VALUES
('P1', 1, 'Programacion', 'Asignatura de DAW, DAM y ASIX'),
('Pr3', 1, 'Proyecto', 'Asignatura de DAW, DAM y ASIX'),
('T4', 1, 'Tutoria', 'Asignatura de DAW, DAM y ASIX'),
('S2', 1, 'Sistemas', 'Asignatura de DAW, DAM y ASIX');

-- Horarios de asignaturas (id_horario_a autoincremental → no se especifica)
INSERT INTO horario_a (id_asignatura, dia, hora, aula)
VALUES
('P1', 'lunes', '15:30', 'Aula 101'),
('S2', 'lunes', '17:00', 'Aula 101'),
('Pr3', 'lunes', '18:00', 'Aula 101'),
('Pr3', 'martes', '17:00', 'Aula 101'),
('T4', 'martes', '19:00', 'Aula 101'),
('P1', 'miercoles', '17:00', 'Aula 101'),
('S2', 'miercoles', '18:00', 'Aula 101'),
('Pr3', 'jueves', '15:30', 'Aula 101'),
('P1', 'jueves', '17:00', 'Aula 101'),
('Pr3', 'viernes', '17:00', 'Aula 101'),
('S2', 'viernes', '18:00', 'Aula 101');

-- Horario de trabajadores (id_horario_t autoincremental → no se especifica)
INSERT INTO horario_t (id_trabajador, fecha, hora)
VALUES
(2, '2025-12-02', '15:00'),
(1, '2025-12-02', '15:00');

-- Asistencia de alumnos
INSERT INTO asiste (id_alumno, id_asignatura, fecha, hora, asistio)
VALUES
(1, 'Pr3', '2025-12-02', '17:00', TRUE),
(2, 'Pr3', '2025-12-02', '17:00', FALSE);
