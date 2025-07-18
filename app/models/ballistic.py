# app/models/ballistic.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
import uuid
from app import db

class DopeEntry(db.Model):
    """DOPE Entry Model - Data On Previous Engagements"""
    
    __tablename__ = 'dope_entries'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    rifle_id = Column(String(36), ForeignKey('rifles.id'), nullable=False)
    ammunition_id = Column(String(36), ForeignKey('ammunition.id'), nullable=False)
    
    # DOPE data
    distance = Column(Integer, nullable=False)
    elevation = Column(String(100), nullable=False)
    windage = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    rifle = db.relationship('Rifle', backref=db.backref('dope_entries', lazy=True))
    ammunition = db.relationship('Ammunition', backref=db.backref('dope_entries', lazy=True))
    
    def __init__(self, user_id, rifle_id, ammunition_id, distance, elevation, windage, **kwargs):
        self.user_id = user_id
        self.rifle_id = rifle_id
        self.ammunition_id = ammunition_id
        self.distance = distance
        self.elevation = elevation
        self.windage = windage
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert DOPE entry to dictionary for JSON response"""
        return {
            'id': self.id,
            'rifleId': self.rifle_id,
            'ammunitionId': self.ammunition_id,
            'distance': self.distance,
            'elevation': self.elevation,
            'windage': self.windage,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save DOPE entry to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete DOPE entry from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_rifle_id(rifle_id):
        """Find all DOPE entries by rifle ID, sorted by distance"""
        return DopeEntry.query.filter_by(rifle_id=rifle_id).order_by(DopeEntry.distance).all()
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all DOPE entries by user ID"""
        return DopeEntry.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(entry_id):
        """Find DOPE entry by ID"""
        return DopeEntry.query.filter_by(id=entry_id).first()


class ZeroEntry(db.Model):
    """Zero Entry Model - Zero tracking entries"""
    
    __tablename__ = 'zero_entries'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    rifle_id = Column(String(36), ForeignKey('rifles.id'), nullable=False)
    
    # Zero data
    distance = Column(Integer, nullable=False)
    poi_offset = Column(String(100), nullable=False)  # Point of Impact offset
    confirmed = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    rifle = db.relationship('Rifle', backref=db.backref('zero_entries', lazy=True))
    
    def __init__(self, user_id, rifle_id, distance, poi_offset, confirmed=False, **kwargs):
        self.user_id = user_id
        self.rifle_id = rifle_id
        self.distance = distance
        self.poi_offset = poi_offset
        self.confirmed = confirmed
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert zero entry to dictionary for JSON response"""
        return {
            'id': self.id,
            'rifleId': self.rifle_id,
            'distance': self.distance,
            'poiOffset': self.poi_offset,
            'confirmed': self.confirmed,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save zero entry to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete zero entry from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_rifle_id(rifle_id):
        """Find all zero entries by rifle ID, sorted by created date (newest first)"""
        return ZeroEntry.query.filter_by(rifle_id=rifle_id).order_by(ZeroEntry.created_at.desc()).all()
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all zero entries by user ID"""
        return ZeroEntry.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(entry_id):
        """Find zero entry by ID"""
        return ZeroEntry.query.filter_by(id=entry_id).first()


class ChronographData(db.Model):
    """Chronograph Data Model - Velocity measurements"""
    
    __tablename__ = 'chronograph_data'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    rifle_id = Column(String(36), ForeignKey('rifles.id'), nullable=False)
    ammunition_id = Column(String(36), ForeignKey('ammunition.id'), nullable=False)
    
    # Chronograph data
    velocities = Column(JSON, nullable=False)  # Array of velocity readings
    average = Column(Float, nullable=False)
    extreme_spread = Column(Float, nullable=False)
    standard_deviation = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    rifle = db.relationship('Rifle', backref=db.backref('chronograph_data', lazy=True))
    ammunition = db.relationship('Ammunition', backref=db.backref('chronograph_data', lazy=True))
    
    def __init__(self, user_id, rifle_id, ammunition_id, velocities, average, extreme_spread, standard_deviation, **kwargs):
        self.user_id = user_id
        self.rifle_id = rifle_id
        self.ammunition_id = ammunition_id
        self.velocities = velocities
        self.average = average
        self.extreme_spread = extreme_spread
        self.standard_deviation = standard_deviation
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert chronograph data to dictionary for JSON response"""
        return {
            'id': self.id,
            'rifleId': self.rifle_id,
            'ammunitionId': self.ammunition_id,
            'velocities': self.velocities,
            'average': self.average,
            'extremeSpread': self.extreme_spread,
            'standardDeviation': self.standard_deviation,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save chronograph data to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete chronograph data from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_rifle_id(rifle_id):
        """Find all chronograph data by rifle ID, sorted by created date (newest first)"""
        return ChronographData.query.filter_by(rifle_id=rifle_id).order_by(ChronographData.created_at.desc()).all()
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all chronograph data by user ID"""
        return ChronographData.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(data_id):
        """Find chronograph data by ID"""
        return ChronographData.query.filter_by(id=data_id).first()


class BallisticCalculation(db.Model):
    """Ballistic Calculation Model - Trajectory calculations"""
    
    __tablename__ = 'ballistic_calculations'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    rifle_id = Column(String(36), ForeignKey('rifles.id'), nullable=False)
    ammunition_id = Column(String(36), ForeignKey('ammunition.id'), nullable=False)
    
    # Calculation parameters
    ballistic_coefficient = Column(Float, nullable=False)
    muzzle_velocity = Column(Float, nullable=False)
    target_distance = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(Float, nullable=False)
    
    # Calculation results (stored as JSON array)
    trajectory_data = Column(JSON, nullable=False)
    
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    rifle = db.relationship('Rifle', backref=db.backref('ballistic_calculations', lazy=True))
    ammunition = db.relationship('Ammunition', backref=db.backref('ballistic_calculations', lazy=True))
    
    def __init__(self, user_id, rifle_id, ammunition_id, ballistic_coefficient, muzzle_velocity, 
                 target_distance, wind_speed, wind_direction, trajectory_data, **kwargs):
        self.user_id = user_id
        self.rifle_id = rifle_id
        self.ammunition_id = ammunition_id
        self.ballistic_coefficient = ballistic_coefficient
        self.muzzle_velocity = muzzle_velocity
        self.target_distance = target_distance
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.trajectory_data = trajectory_data
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert ballistic calculation to dictionary for JSON response"""
        return {
            'id': self.id,
            'rifleId': self.rifle_id,
            'ammunitionId': self.ammunition_id,
            'ballisticCoefficient': self.ballistic_coefficient,
            'muzzleVelocity': self.muzzle_velocity,
            'targetDistance': self.target_distance,
            'windSpeed': self.wind_speed,
            'windDirection': self.wind_direction,
            'trajectoryData': self.trajectory_data,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save ballistic calculation to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete ballistic calculation from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_rifle_id(rifle_id):
        """Find all ballistic calculations by rifle ID, sorted by created date (newest first)"""
        return BallisticCalculation.query.filter_by(rifle_id=rifle_id).order_by(BallisticCalculation.created_at.desc()).all()
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all ballistic calculations by user ID"""
        return BallisticCalculation.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(calculation_id):
        """Find ballistic calculation by ID"""
        return BallisticCalculation.query.filter_by(id=calculation_id).first()