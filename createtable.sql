-- Table for TLE (Two-Line Element) Data
CREATE TABLE SatelliteTLE (
    SatelliteName VARCHAR(255),
    SatelliteID INT AUTO_INCREMENT PRIMARY KEY,
    NoradCatalogNumber INT,
    InternationalDesignator VARCHAR(10),
    EpochDate DECIMAL(15,8),
    BStarDrag DECIMAL(13,10),
    Inclination DECIMAL(8,4),
    RightAscensionOfAscendingNode DECIMAL(8,4),
    Eccentricity DECIMAL(10,8),
    ArgumentOfPerigee DECIMAL(8,4),
    MeanAnomaly DECIMAL(8,4),
    MeanMotion DECIMAL(11,8),
    Revolutions INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table for OMM (Orbital Mean Motion) Data
CREATE TABLE SatelliteOMM (
    satellite_id INT PRIMARY KEY,
    object_name VARCHAR(255),
    object_id VARCHAR(20),
    center_name VARCHAR(50),
    ref_frame VARCHAR(20),
    time_system VARCHAR(10),
    mean_element_theory VARCHAR(20)
);

-- Table for Detailed Orbit Information
CREATE TABLE OrbitOMM (
    orbit_id INT AUTO_INCREMENT PRIMARY KEY,
    satellite_id INT,
    epoch DATETIME,
    mean_motion DECIMAL(18, 8),
    eccentricity DECIMAL(18, 7),
    inclination DECIMAL(18, 4),
    ra_of_asc_node DECIMAL(18, 4),
    arg_of_pericenter DECIMAL(18, 4),
    mean_anomaly DECIMAL(18, 4),
    ephemeris_type INT,
    classification_type CHAR(1),
    norad_cat_id INT,
    element_set_no INT,
    rev_at_epoch INT,
    bstar DECIMAL(18, 12),
    mean_motion_dot DECIMAL(18, 12),
    mean_motion_ddot DECIMAL(18, 12),
    FOREIGN KEY (satellite_id) REFERENCES SatelliteOMM(satellite_id)
);
