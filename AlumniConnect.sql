CREATE DATABASE IF NOT  EXISTS AlumniConnect;
USE AlumniConnect;
CREATE TABLE IF NOT EXISTS users (
   id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    date_of_birth DATE,
    address TEXT,
    institute_name VARCHAR(255),
    name_of_degree VARCHAR(100),
    graduation_year YEAR,
    major_field_of_study VARCHAR(100),
    achievements TEXT,
    current_employer VARCHAR(255),
    work_experience TEXT,
    professional_field VARCHAR(100),
    job_title VARCHAR(100),
    skills TEXT,
    certificates TEXT,
    languages_spoken TEXT
);

SELECT* FROM users;
SHOW TABLEs ;
