from django.db import connection

def create_all_tables():
    createqueries1 = [
        """CREATE TABLE IF NOT EXISTS warehouse (
            warehouseid INT PRIMARY KEY,
            address VARCHAR(155) NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS retailer (
            name VARCHAR(65) PRIMARY KEY,
            acceptedgrade CHAR(1) NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS supplier (
            name VARCHAR(65) PRIMARY KEY
        );""",
        """CREATE TABLE IF NOT EXISTS warehouse_distribution (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            warehouseid INT,
            supname VARCHAR(65),
            FOREIGN KEY (warehouseid) REFERENCES warehouse(warehouseid),
            FOREIGN KEY (supname) REFERENCES supplier(name),
            UNIQUE (id, warehouseid, supname, date)
        );""",

        """CREATE TABLE IF NOT EXISTS product (
            product_ID INT AUTO_INCREMENT PRIMARY KEY,
            product_Name VARCHAR(55) NOT NULL UNIQUE,
            product_Type VARCHAR(20) NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS government_specialist (
            specialist_id INT AUTO_INCREMENT PRIMARY KEY,
            designation VARCHAR(255) NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS specialist_license (
            id INT AUTO_INCREMENT PRIMARY KEY,
            specialist_id INT NOT NULL,
            degree_name VARCHAR(255) NOT NULL,
            date_received DATE NOT NULL,
            FOREIGN KEY (specialist_id) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS inspector (
            IspecialistID INT PRIMARY KEY,
            FOREIGN KEY (IspecialistID) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS nutrition_specialist (
            NspecialistID INT PRIMARY KEY,
            FOREIGN KEY (NspecialistID) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS harvested_produce (
            batch_id INT AUTO_INCREMENT PRIMARY KEY,
            sowing_date DATE NOT NULL,
            harvest_date DATE NOT NULL,
            weight FLOAT NOT NULL,
            smoothness VARCHAR(50) NOT NULL,
            colour VARCHAR(50) NOT NULL,
            fungal_growth BOOLEAN NOT NULL,
            weather_conditions VARCHAR(255) NOT NULL,
            pesticides_used BOOLEAN NOT NULL,
            nutrionistID INT NOT NULL, 
            produceID INT NOT NULL,    
            FOREIGN KEY (nutrionistID) REFERENCES nutrition_specialist(NspecialistID) ON DELETE CASCADE,
            FOREIGN KEY (produceID) REFERENCES product(product_ID) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS farm (
            registration_id VARCHAR(100) PRIMARY KEY,
            size FLOAT NOT NULL,
            address VARCHAR(255) NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS farm_production (
            id INT AUTO_INCREMENT PRIMARY KEY,
            batch_id INT NOT NULL,
            registration_id VARCHAR(100) NOT NULL,
            FOREIGN KEY (batch_id) REFERENCES harvested_produce(batch_id) ON DELETE CASCADE,
            FOREIGN KEY (registration_id) REFERENCES farm(registration_id) ON DELETE CASCADE,
            CONSTRAINT unique_batch_farm UNIQUE (batch_id, registration_id)
        );""",
    
        """CREATE TABLE IF NOT EXISTS warehouse_cert (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_received DATE,
            expiry_date DATE,
            name_of_certification VARCHAR(55) NOT NULL,
            warehouse_id INT NOT NULL,
            inspector_id INT NOT NULL,
            FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouseid) ON DELETE CASCADE,
            FOREIGN KEY (inspector_id) REFERENCES inspector(IspecialistID) ON DELETE CASCADE,
            CONSTRAINT unique_certification_date UNIQUE (name_of_certification, date_received)
        );""",


        """CREATE TABLE IF NOT EXISTS vehicle_gps_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        vehicle_id INT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        speed FLOAT,
        altitude FLOAT,
        heading FLOAT,
        FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
        );""",

        """CREATE TABLE IF NOT EXISTS  coordinates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gps_log_id INT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    FOREIGN KEY (gps_log_id) REFERENCES vehicle_gps_log(id)
        );""",


        """CREATE TABLE IF NOT EXISTS logistics_company (
            company_name VARCHAR(255) PRIMARY KEY,
            road VARCHAR(25) NOT NULL,
            area VARCHAR(55) NOT NULL
        );""",

          """CREATE TABLE IF NOT EXISTS vehicle (
            vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
            registration_plate_no VARCHAR(15) UNIQUE NOT NULL,
            model VARCHAR(100) NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            max_capacity FLOAT NOT NULL,
            FOREIGN KEY (company_name) REFERENCES logistics_company(company_name) ON DELETE CASCADE,
            gps_tracking_number VARCHAR(50) UNIQUE NOT NULL
        );""",


        """CREATE TABLE IF NOT EXISTS packing_facility (
            facID SMALLINT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            capacity INT NOT NULL,
            street VARCHAR(50) NOT NULL,
            area VARCHAR(100) NOT NULL
        );""",

        """CREATE TABLE IF NOT EXISTS facility_certification (
            certification_id INT AUTO_INCREMENT PRIMARY KEY,
            certification_name VARCHAR(255) NOT NULL,
            expiry_date DATE NOT NULL,
            facID SMALLINT NOT NULL,
            FOREIGN KEY (facID) REFERENCES packing_facility(facID) ON DELETE CASCADE,
            CONSTRAINT unique_certification_name_facility_expiry UNIQUE (certification_name, facID, expiry_date)
        );""",
        
        """CREATE TABLE IF NOT EXISTS delivery_harvested (
            delivery_id INT AUTO_INCREMENT PRIMARY KEY,
            transport_date DATE NOT NULL,
            quantity FLOAT NOT NULL,
            temperature FLOAT NOT NULL,
            humidity FLOAT NOT NULL,
            cost FLOAT NOT NULL,
            facility_id SMALLINT NOT NULL,
            vehicle_id INT NOT NULL,
            batch_id INT NOT NULL,
            FOREIGN KEY (facility_id) REFERENCES packing_facility(facID) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id) ON DELETE CASCADE,
            FOREIGN KEY (batch_id) REFERENCES harvested_produce(batch_id) ON DELETE CASCADE
        );""",
        
        """CREATE TABLE IF NOT EXISTS packed_produce (
            barcode VARCHAR(50) PRIMARY KEY,
            weight FLOAT NOT NULL,
            material VARCHAR(100) NOT NULL,
            cost_per_unit FLOAT NOT NULL,
            facilityID SMALLINT NULL,
            FOREIGN KEY (facilityID) REFERENCES packing_facility(facID) ON DELETE CASCADE,
        );""",
        
        """CREATE TABLE IF NOT EXISTS delivery_of_packed (
            delivery_id INT AUTO_INCREMENT PRIMARY KEY,
            transport_date DATE NOT NULL,
            quantity FLOAT NOT NULL,
            temperature FLOAT NOT NULL,
            cost FLOAT NOT NULL,
            warehouse_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            barcode VARCHAR(50) NOT NULL,
            FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouseid) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id) ON DELETE CASCADE,
            FOREIGN KEY (barcode) REFERENCES packed_produce(barcode) ON DELETE CASCADE
        );""",
        
        """CREATE TABLE IF NOT EXISTS nutrition_content_report (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fat_content FLOAT NOT NULL,
            sugar_content FLOAT NOT NULL,
            vitamin_content FLOAT NOT NULL,
            mineral_content FLOAT NOT NULL,
            nutritionist_id INT NOT NULL,
            barcode VARCHAR(50) NOT NULL,
            FOREIGN KEY (nutritionist_id) REFERENCES nutrition_specialist(NspecialistID) ON DELETE CASCADE,
            FOREIGN KEY (barcode) REFERENCES packed_produce(barcode) ON DELETE CASCADE,
            CONSTRAINT unique_nutritionist_barcode UNIQUE (nutritionist_id, barcode)
        );""",
        
        """CREATE TABLE IF NOT EXISTS inspection_report (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_received DATE NOT NULL,
            date_expired DATE NOT NULL,
            ventilation INT NOT NULL,
            cleanliness INT NOT NULL,
            inspector_id INT NOT NULL,
            vehicle_id INT NOT NULL,
            FOREIGN KEY (inspector_id) REFERENCES inspector(IspecialistID) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id) ON DELETE CASCADE,
            CONSTRAINT unique_inspector_vehicle_date UNIQUE (inspector_id, vehicle_id, date_received)
        );""",

        """ CREATE TABLE IF NOT EXISTS packing_facility_cert (
            id INT AUTO_INCREMENT PRIMARY KEY,
            certificateName VARCHAR(55) NOT NULL,
            date_received DATE NOT NULL,
            facilityID SMALLINT NOT NULL,
            specialistID INT NOT NULL,
            FOREIGN KEY (facilityID) REFERENCES packing_facility(facID) ON DELETE CASCADE,
            FOREIGN KEY (specialistID) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE,
            CONSTRAINT unique_certificate UNIQUE (certificateName, facilityID, date_received)
        );"""

    ]

    with connection.cursor() as cursor:
        for query in createqueries1:
            cursor.execute(query)
        

def insert1():
    insertwofk = [
        """INSERT IGNORE INTO packed_produce (barcode, weight, material, cost_per_unit)
        VALUES
        ('B001', 10.5, 'Plastic', 15.25),
        ('B002', 12.0, 'Glass', 20.50),
        ('B003', 8.3, 'Plastic', 18.75),
        ('B004', 15.0, 'Wood', 22.00),
        ('B005', 7.5, 'Metal', 19.00),
        ('B006', 10.0, 'Cardboard', 12.50),
        ('B007', 11.0, 'Plastic', 16.00),
        ('B008', 9.8, 'Glass', 21.00),
        ('B009', 13.2, 'Metal', 17.50),
        ('B010', 14.5, 'Wood', 23.00);
        """,

        """INSERT IGNORE INTO warehouse (warehouseid, address) VALUES
        (1, 'New Eskaton Road, Dhaka'),
        (2, '123, Mirpur Road, Dhaka'),
        (3, '45, Kazi Nazrul Islam Avenue, Dhaka'),
        (4, '789, Rampura Bazar, Dhaka'),
        (5, '32, Sylhet Road, Moulvibazar')""",

        """INSERT IGNORE INTO retailer (name, acceptedgrade) VALUES
        ('Rahim Store', 'A'),
        ('Hossain Mart', 'B'),
        ('Karim Retailers', 'A'),
        ('Jamil Superstore', 'C'),
        ('Hasan & Sons', 'B');""",

        """INSERT IGNORE  INTO supplier (name) VALUES
        ('Aftab Foods Ltd.'),
        ('Bangladesh Rice & Oil Co.'),
        ('Golden Harvest Ltd.'),
        ('Fresh Farms Ltd.'),
        ('Greenfields Ltd.');""",

        """INSERT IGNORE INTO product (product_Name, product_Type) VALUES
        ('Rice', 'Non-Perishable'),
        ('Wheat', 'Non-Perishable'),
        ('Potato', 'Perishable'),
        ('Tomato', 'Perishable'),
        ('Apple', 'Perishable');""",

        """INSERT IGNORE INTO government_specialist (designation) VALUES
        ('Inspector'),
        ('Nutrition_Specialist'),
        ('Inspector'),
        ('Nutrition_Specialist'),
        ('Inspector');""",

        """INSERT IGNORE INTO farm (registration_id, size, address) VALUES
        ('FARM-1001', 25.5, 'Bashundhara, Dhaka'),
        ('FARM-1002', 30.0, 'Mirpur, Dhaka'),
        ('FARM-1003', 40.0, 'Chattogram'),
        ('FARM-1004', 12.5, 'Sylhet'),
        ('FARM-1005', 55.0, 'Rajshahi');""",

        """INSERT IGNORE  INTO packing_facility (facID, name, capacity, street, area) VALUES
        (1, 'FreshPack Ltd.', 500, '123, Industrial Area', 'Khilgaon, Dhaka'),
        (2, 'GreenPack Corp.', 1000, '45, Agricultural Road', 'Narsingdi, Dhaka'),
        (3, 'PurePack Industries', 750, '78, Packing Lane', 'Madaripur'),
        (4, 'CityPack Ltd.', 800, '32, West Road', 'Mirpur, Dhaka'),
        (5, 'PackIt Pvt. Ltd.', 600, '6, Main Street', 'Chandpur');"""
    ]

    with connection.cursor() as cursor:
        for q in insertwofk:
            cursor.execute(q)

def insert2():
    insertwfk = [

        """INSERT INTO farm_production (batch_id, registration_id)
            VALUES 
                (5255, 'FARM-1001'),
                (5256, 'FARM-1002'),
                (5257, 'FARM-1003'),
                (5258, 'FARM-1004'),
                (5259, 'FARM-1005'),
                (5260, 'FARM-1001'),
                (5261, 'FARM-1002'),
                (5262, 'FARM-1003'),
                (5263, 'FARM-1004'),
                (5264, 'FARM-1005'),
                (5265, 'FARM-1001'),
                (5266, 'FARM-1002'),
                (5267, 'FARM-1003'),
                (5268, 'FARM-1004'),
                (5269, 'FARM-1005');
            """,

        """INSERT IGNORE INTO nutrition_content_report (fat_content, sugar_content, vitamin_content, mineral_content, nutritionist_id, barcode)
        VALUES
        (5.2, 3.1, 7.8, 12.5, 1, 'B001'),
        (4.5, 2.7, 6.9, 9.2, 2, 'B002'),
        (3.4, 4.0, 8.3, 10.1, 3, 'B003'),
        (6.1, 1.5, 9.0, 15.0, 4, 'B004'),
        (2.9, 3.5, 7.2, 8.8, 5, 'B005'),
        (4.8, 2.9, 7.5, 11.4, 1, 'B006'),
        (5.3, 3.3, 6.4, 13.2, 2, 'B007'),
        (4.2, 3.8, 8.1, 9.6, 3, 'B008'),
        (6.0, 2.6, 7.0, 14.3, 4, 'B009'),
        (3.5, 4.1, 7.3, 12.7, 5, 'B010');
        """,
              
        """INSERT IGNORE  INTO warehouse_distribution (date, warehouseid, supname) VALUES
        ('2024-01-01', 1, 'Aftab Foods Ltd.'),
        ('2024-02-01', 2, 'Bangladesh Rice & Oil Co.'),
        ('2024-03-01', 3, 'Golden Harvest Ltd.'),
        ('2024-04-01', 4, 'Fresh Farms Ltd.'),
        ('2024-05-01', 5, 'Greenfields Ltd.'),
        ('2024-06-01', 1, 'Fresh Farms Ltd.'),
        ('2024-07-01', 2, 'Aftab Foods Ltd.'),
        ('2024-08-01', 3, 'Greenfields Ltd.'),
        ('2024-09-01', 4, 'Golden Harvest Ltd.'),
        ('2024-10-01', 5, 'Bangladesh Rice & Oil Co.');""",

        """ INSERT IGNORE INTO warehouse_cert (date_received, expiry_date, name_of_certification, warehouse_id, inspector_id) VALUES
        ('2024-01-01', '2025-01-01', 'ISO 9001', 1, 1),
        ('2024-02-01', '2025-02-01', 'HACCP Certification', 2, 2),
        ('2024-03-01', '2025-03-01', 'GMP Certification', 3, 3),
        ('2024-04-01', '2025-04-01', 'ISO 22000', 4, 4),
        ('2024-05-01', '2025-05-01', 'FSSC 22000', 5, 5),
        ('2024-06-01', '2025-06-01', 'BRC Certification', 1, 2),
        ('2024-07-01', '2025-07-01', 'SQF Certification', 2, 3),
        ('2024-08-01', '2025-08-01', 'KOSHER Certification', 3, 4),
        ('2024-09-01', '2025-09-01', 'Halal Certification', 4, 5),
        ('2024-10-01', '2025-10-01', 'GlobalGAP', 5, 1);""",

        """ INSERT IGNORE INTO vehicle (registration_plate_no, model, max_capacity, gps_tracking_number) VALUES
        ('ABC-1001', 'Freightliner Cascadia', 22.0, 'GPS1234FREIGHT'),
        ('XYZ-2002', 'Volvo refrigerated VNL 740', 20.0, 'GPS5678VOLVO'),
        ('LMN-3003', 'Kenworth T680', 21.0, 'GPS9101KENWORTH'),
        ('PQR-4004', 'Peterbilt 579', 22.5, 'GPS1121PETERBILT'),
        ('DEF-5005', 'International LT Series', 23.0, 'GPS3141INTERNATIONAL'),
        ('JKL-6006', 'Mack REEFER Truck', 20.5, 'GPS5161MACK');""",

        """INSERT IGNORE INTO vehicle_gps_log (vehicle_id, timestamp, speed, altitude, heading) VALUES
        (1, '2024-12-11 14:00:00', 60.0, 150.0, 90.0),
        (2, '2024-12-11 14:15:00', 70.5, 200.0, 180.0),
        (3, '2024-12-11 14:30:00', 55.3, 500.0, 270.0),
        (4, '2024-12-11 14:45:00', 80.0, 1200.0, 360.0),
        (1, '2024-12-11 15:00:00', 45.0, 50.0, 120.0),
        (2, '2024-12-11 15:15:00', 65.5, 750.0, 240.0),
        (3, '2024-12-11 15:30:00', 72.3, 1000.0, 60.0),
        (4, '2024-12-11 15:45:00', 58.7, 800.0, 330.0),
        (1, '2024-12-11 16:00:00', 77.0, 1100.0, 210.0),
        (2, '2024-12-11 16:15:00', 50.3, 300.0, 30.0);""",

        """INSERT IGNORE  INTO coordinates (gps_log_id, latitude, longitude) VALUES
        (1, 23.8103, 90.4125),
        (1, 23.8110, 90.4130),
        (2, 23.8120, 90.4140),
        (2, 23.8130, 90.4150),
        (3, 23.8140, 90.4160),
        (3, 23.8150, 90.4170),
        (4, 23.8160, 90.4180),
        (4, 23.8170, 90.4190),
        (5, 23.8180, 90.4200),
        (5, 23.8190, 90.4210),
        (6, 23.8200, 90.4220),
        (6, 23.8210, 90.4230),
        (7, 23.8220, 90.4240),
        (7, 23.8230, 90.4250),
        (8, 23.8240, 90.4260);""",

        """INSERT IGNORE INTO logistics_company (company_name, road, area) VALUES
        ('LogiCo', 'Main St', 'Dhaka'),
        ('SpeedEx', 'Oxford Road', 'Chittagong'),
        ('TransFast', 'Sunset Blvd', 'Sylhet'),
        ('QuickMove', 'Elm Street', 'Mymensingh'),
        ('CargoPlus', 'Highway 1', 'Rajshahi');""",

      

        """INSERT IGNORE  INTO specialist_license (specialist_id, degree_name, date_received) VALUES
        (1, 'Master of Science in Food Safety', '2023-06-15'),
        (2, 'PhD in Agriculture', '2022-08-10'),
        (3, 'Bachelor of Science in Environmental Health', '2021-09-21'),
        (4, 'Master of Public Health', '2020-05-30'),
        (5, 'PhD in Nutrition', '2023-01-10'),
        (1, 'Master of Science in Food Safety', '2024-04-15'),
        (2, 'Bachelor of Science in Agriculture', '2023-11-11'),
        (3, 'PhD in Environmental Health', '2022-07-19'),
        (4, 'Master of Public Health', '2021-10-20'),
        (5, 'PhD in Nutrition', '2023-12-02');""",

        """INSERT IGNORE  INTO inspector (IspecialistID) VALUES
        (1),
        (2),
        (3),
        (4),
        (5),
        (1),
        (2),
        (3),
        (4),
        (5);""",

    
        """INSERT IGNORE  INTO nutrition_specialist (NspecialistID) VALUES
        (1),
        (2),
        (3),
        (4),
        (5),
        (1),
        (2),
        (3),
        (4),
        (5);""",

        """INSERT IGNORE  INTO harvested_produce (sowing_date, harvest_date, weight, smoothness, colour, fungal_growth, weather_conditions, pesticides_used, nutrionistID, produceID) VALUES
        ('2023-03-01', '2023-06-01', 25.4, 'Smooth', 'Green', FALSE, 'Sunny', TRUE, 1, 2476),
        ('2023-02-15', '2023-05-10', 18.7, 'Rough', 'Red', TRUE, 'Cloudy', FALSE, 2, 2477),
        ('2023-04-01', '2023-07-01', 30.2, 'Smooth', 'Yellow', FALSE, 'Windy', TRUE, 3, 2478),
        ('2023-03-10', '2023-06-15', 22.1, 'Smooth', 'Purple', FALSE, 'Sunny', FALSE, 4, 2479),
        ('2023-01-05', '2023-04-10', 20.5, 'Rough', 'Green', TRUE, 'Rainy', TRUE, 5, 2480),
        ('2023-05-15', '2023-08-15', 28.3, 'Smooth', 'Orange', FALSE, 'Windy', TRUE, 1, 2486),
        ('2023-02-20', '2023-05-25', 24.7, 'Rough', 'Blue', TRUE, 'Cloudy', FALSE, 2, 2487),
        ('2023-04-15', '2023-07-20', 32.0, 'Smooth', 'Pink', FALSE, 'Sunny', TRUE, 3, 2488),
        ('2023-03-25', '2023-06-30', 18.2, 'Smooth', 'Red', FALSE, 'Cloudy', FALSE, 4, 2489),
        ('2023-06-01', '2023-09-01', 27.4, 'Rough', 'Yellow', TRUE, 'Rainy', TRUE, 5, 2490),
        ('2023-01-20', '2023-04-20', 35.0, 'Smooth', 'Green', FALSE, 'Windy', FALSE, 1, 2491),
        ('2023-02-25', '2023-05-30', 26.8, 'Rough', 'Purple', TRUE, 'Sunny', TRUE, 2, 2492),
        ('2023-05-10', '2023-08-10', 29.5, 'Smooth', 'Orange', FALSE, 'Cloudy', FALSE, 3, 2493),
        ('2023-03-12', '2023-06-12', 23.3, 'Rough', 'Blue', TRUE, 'Windy', TRUE, 4, 2476),
        ('2023-04-05', '2023-07-10', 19.9, 'Smooth', 'Pink', FALSE, 'Rainy', TRUE, 5, 2477),
        ('2023-05-20', '2023-08-20', 33.1, 'Rough', 'Green', TRUE, 'Sunny', FALSE, 1, 2478),
        ('2023-01-10', '2023-04-12', 21.4, 'Smooth', 'Red', FALSE, 'Cloudy', TRUE, 2, 2479),
        ('2023-06-01', '2023-09-05', 28.0, 'Rough', 'Yellow', TRUE, 'Windy', FALSE, 3, 2480),
        ('2023-02-10', '2023-05-10', 20.6, 'Smooth', 'Purple', FALSE, 'Rainy', TRUE, 4, 2486),
        ('2023-03-22', '2023-06-30', 24.2, 'Rough', 'Blue', TRUE, 'Sunny', FALSE, 5, 2487);""",

        """INSERT INTO delivery_harvested (transport_date, quantity, temperature, humidity, cost, facility_id, vehicle_id, batch_id)
        VALUES
        ('2024-12-01', 150.0, 20.5, 80.0, 250.00, 1, 1, 5255),
        ('2024-12-02', 180.0, 22.0, 85.0, 270.00, 2, 2, 5255),
        ('2024-12-03', 200.0, 21.0, 82.0, 290.00, 3, 3, 5257),
        ('2024-12-04', 170.0, 19.0, 78.0, 260.00, 4, 4, 5258),
        ('2024-12-05', 160.0, 23.0, 79.0, 280.00, 5, 5, 5259),
        ('2024-12-06', 190.0, 18.5, 81.0, 300.00, 5, 6, 5260),
        ('2024-12-07', 210.0, 20.0, 83.0, 310.00, 1, 2, 5261),
        ('2024-12-08', 175.0, 22.5, 80.0, 275.00, 2, 3, 5262),
        ('2024-12-09', 185.0, 21.5, 79.5, 285.00, 3, 4, 5263),
        ('2024-12-10', 195.0, 24.0, 84.0, 320.00, 4, 5, 5264),
        ('2024-12-11', 205.0, 19.5, 77.0, 295.00, 5, 6, 5265),
        ('2024-12-12', 215.0, 22.0, 86.0, 330.00, 2, 1, 5266),
        ('2024-12-13', 220.0, 23.5, 80.5, 340.00, 1, 2, 5267),
        ('2024-12-14', 230.0, 21.0, 79.0, 350.00, 2, 3, 5268),
        ('2024-12-15', 240.0, 20.0, 78.0, 360.00, 3, 4, 5269),
        ('2024-12-16', 250.0, 19.0, 81.0, 370.00, 4, 5, 5270),
        ('2024-12-17', 260.0, 22.5, 82.5, 380.00, 5, 6, 5271),
        ('2024-12-18', 270.0, 23.0, 84.0, 390.00, 5, 1, 5272),
        ('2024-12-19', 280.0, 21.5, 85.0, 400.00, 1, 2, 5273),
        ('2024-12-20', 290.0, 20.5, 83.0, 410.00, 2, 3, 5274);
        """,

        """ INSERT INTO delivery_of_packed (transport_date, quantity, temperature, cost, warehouse_id, vehicle_id, barcode) 
            VALUES
            ('2023-03-01', 150.5, 22.5, 1000.0, 1, 1, 'B001'),
            ('2023-03-03', 200.2, 20.0, 1200.0, 2, 2, 'B002'),
            ('2023-03-05', 180.3, 23.0, 1100.5, 3, 3, 'B003'),
            ('2023-03-07', 220.7, 21.5, 1300.0, 4, 4, 'B004'),
            ('2023-03-09', 170.4, 25.0, 1150.0, 5, 5, 'B005'),
            ('2023-03-11', 160.0, 24.0, 1050.0, 6, 6, 'B006'),
            ('2023-03-13', 140.2, 22.0, 950.0, 7, 1, 'B007'),
            ('2023-03-15', 210.3, 21.0, 1250.0, 8, 2, 'B008'),
            ('2023-03-17', 230.8, 23.5, 1350.0, 9, 3, 'B009'),
            ('2023-03-19', 190.4, 20.5, 1200.0, 10, 4, 'B010'),
            ('2023-03-21', 220.1, 22.0, 1305.0, 1, 5, 'B001'),
            ('2023-03-23', 200.7, 24.5, 1180.0, 2, 6, 'B002'),
            ('2023-03-25', 160.3, 23.0, 1085.0, 3, 1, 'B003'),
            ('2023-03-27', 210.5, 21.5, 1230.0, 4, 2, 'B004'),
            ('2023-03-29', 180.6, 22.5, 1120.0, 5, 3, 'B005');
            """


    ]

    with connection.cursor() as cursor:
        for q in insertwfk:
            cursor.execute(q)
