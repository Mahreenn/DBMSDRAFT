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
            IspecialistID INT PRIMARY KEY
            FOREIGN KEY (IspecialistID) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE
        );""",

        """CREATE TABLE IF NOT EXISTS nutrition_specialist (
            NspecialistID INT PRIMARY KEY
            FOREIGN KEY (Nspecialist_id) REFERENCES government_specialist(specialist_id) ON DELETE CASCADE
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
            vehicle_id INT NOT NULL,
            timestamp DATETIME NOT NULL,
            speed FLOAT,
            altitude FLOAT,
            heading FLOAT,
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id) ON DELETE CASCADE
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
        

