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
            UNIQUE (warehouseid, supname, date)
        );""",


        """CREATE TABLE IF NOT EXISTS product (
            product_ID INT AUTO_INCREMENT PRIMARY KEY,
            product_Name VARCHAR(55) NOT NULL,
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

        """CREATE TABLE IF NOT EXISTS vehicle (
            vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
            registration_plate_no VARCHAR(15) UNIQUE NOT NULL,
            model VARCHAR(100) NOT NULL,
            max_capacity FLOAT NOT NULL,
            gps_tracking_number VARCHAR(50) UNIQUE NOT NULL
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

        """CREATE TABLE IF NOT EXISTS logistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            vehicle_id INT NOT NULL,
            FOREIGN KEY (company_name) REFERENCES logistics_company(company_name) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id) ON DELETE CASCADE
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
        );"""
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
            cost_per_unit FLOAT NOT NULL
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
            ventilation VARCHAR(55) NOT NULL,
            cleanliness VARCHAR(55) NOT NULL,
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
        ('2023-01-10', '2023-05-20', 1500, 'Smooth', 'Yellow', FALSE, 'Sunny', FALSE, 1, 1),
        ('2023-02-15', '2023-06-10', 2000, 'Smooth', 'Brown', FALSE, 'Cloudy', TRUE, 2, 2),
        ('2023-03-25', '2023-07-05', 1200, 'Rough', 'Red', TRUE, 'Rainy', TRUE, 3, 3),
        ('2023-04-10', '2023-08-12', 1600, 'Smooth', 'Green', FALSE, 'Sunny', FALSE, 4, 4),
        ('2023-05-05', '2023-09-02', 1700, 'Smooth', 'Red', FALSE, 'Cloudy', TRUE, 5, 5),
        ('2023-06-18', '2023-10-03', 1800, 'Smooth', 'Yellow', FALSE, 'Rainy', FALSE, 1, 1),
        ('2023-07-22', '2023-11-12', 1400, 'Rough', 'Yellow', TRUE, 'Sunny', TRUE, 2, 2),
        ('2023-08-10', '2023-12-01', 2100, 'Smooth', 'Green', FALSE, 'Cloudy', FALSE, 3, 3),
        ('2023-09-15', '2024-01-10', 1900, 'Smooth', 'Red', FALSE, 'Rainy', TRUE, 4, 4),
        ('2023-10-05', '2024-02-15', 1300, 'Rough', 'Yellow', TRUE, 'Sunny', FALSE, 5, 5);"""


    ]

    with connection.cursor() as cursor:
        for q in insertwfk:
            cursor.execute(q)
