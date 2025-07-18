# app/models/loadout.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from app import db

class Rifle(db.Model):
    """Rifle Model - Represents rifles in the system"""
    
    __tablename__ = 'rifles'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    generation_variant = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    caliber = Column(String(100), nullable=False)
    
    # Barrel information (stored as JSON)
    barrel = Column(JSON, nullable=True)
    
    # Action information (stored as JSON)
    action = Column(JSON, nullable=True)
    
    # Stock information (stored as JSON)
    stock = Column(JSON, nullable=True)
    
    # Associated scope and ammunition IDs
    scope_id = Column(String(36), ForeignKey('scopes.id'), nullable=True)
    ammunition_id = Column(String(36), ForeignKey('ammunition.id'), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Advanced fields
    serial_number = Column(String(255), nullable=True)
    overall_length = Column(String(100), nullable=True)
    weight = Column(String(100), nullable=True)
    capacity = Column(String(100), nullable=True)
    finish = Column(String(255), nullable=True)
    sight_type = Column(String(255), nullable=True)
    sight_optic = Column(String(255), nullable=True)
    sight_model = Column(String(255), nullable=True)
    sight_height = Column(String(100), nullable=True)
    purchase_date = Column(String(100), nullable=True)
    modifications = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    scope = db.relationship('Scope', backref='rifles_using', lazy=True)
    ammunition = db.relationship('Ammunition', backref='rifles_using', lazy=True)
    
    def __init__(self, user_id, name, brand, manufacturer, generation_variant, model, caliber, **kwargs):
        self.user_id = user_id
        self.name = name
        self.brand = brand
        self.manufacturer = manufacturer
        self.generation_variant = generation_variant
        self.model = model
        self.caliber = caliber
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert rifle to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'manufacturer': self.manufacturer,
            'generationVariant': self.generation_variant,
            'model': self.model,
            'caliber': self.caliber,
            'barrel': self.barrel,
            'action': self.action,
            'stock': self.stock,
            'scope': self.scope.to_dict() if self.scope else None,
            'ammunition': self.ammunition.to_dict() if self.ammunition else None,
            'isActive': self.is_active,
            'notes': self.notes,
            'serialNumber': self.serial_number,
            'overallLength': self.overall_length,
            'weight': self.weight,
            'capacity': self.capacity,
            'finish': self.finish,
            'sightType': self.sight_type,
            'sightOptic': self.sight_optic,
            'sightModel': self.sight_model,
            'sightHeight': self.sight_height,
            'purchaseDate': self.purchase_date,
            'modifications': self.modifications,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save rifle to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete rifle from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all rifles by user ID"""
        return Rifle.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(rifle_id):
        """Find rifle by ID"""
        return Rifle.query.filter_by(id=rifle_id).first()
    
    @staticmethod
    def find_active_by_user_id(user_id):
        """Find active rifle by user ID"""
        return Rifle.query.filter_by(user_id=user_id, is_active=True).first()


class Ammunition(db.Model):
    """Ammunition Model - Represents ammunition in the system"""
    
    __tablename__ = 'ammunition'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    caliber = Column(String(100), nullable=False)
    
    # Bullet information (stored as JSON)
    bullet = Column(JSON, nullable=True)
    
    # Basic load data
    powder = Column(String(255), nullable=True)
    primer = Column(String(255), nullable=True)
    brass = Column(String(255), nullable=True)
    velocity = Column(Integer, nullable=True)
    es = Column(Integer, nullable=True)  # Extreme Spread
    sd = Column(Integer, nullable=True)  # Standard Deviation
    lot_number = Column(String(255), nullable=True)
    count = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=True)
    temp_stable = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Advanced fields
    cartridge_type = Column(String(255), nullable=True)
    case_material = Column(String(255), nullable=True)
    primer_type = Column(String(255), nullable=True)
    pressure_class = Column(String(255), nullable=True)
    sectional_density = Column(Float, nullable=True)
    recoil_energy = Column(Float, nullable=True)
    powder_charge = Column(Float, nullable=True)
    powder_type = Column(String(255), nullable=True)
    chronograph_fps = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, name, manufacturer, caliber, count=0, temp_stable=False, **kwargs):
        self.user_id = user_id
        self.name = name
        self.manufacturer = manufacturer
        self.caliber = caliber
        self.count = count
        self.temp_stable = temp_stable
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert ammunition to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'manufacturer': self.manufacturer,
            'caliber': self.caliber,
            'bullet': self.bullet,
            'powder': self.powder,
            'primer': self.primer,
            'brass': self.brass,
            'velocity': self.velocity,
            'es': self.es,
            'sd': self.sd,
            'lotNumber': self.lot_number,
            'count': self.count,
            'price': self.price,
            'tempStable': self.temp_stable,
            'notes': self.notes,
            'cartridgeType': self.cartridge_type,
            'caseMaterial': self.case_material,
            'primerType': self.primer_type,
            'pressureClass': self.pressure_class,
            'sectionalDensity': self.sectional_density,
            'recoilEnergy': self.recoil_energy,
            'powderCharge': self.powder_charge,
            'powderType': self.powder_type,
            'chronographFPS': self.chronograph_fps,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save ammunition to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete ammunition from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all ammunition by user ID"""
        return Ammunition.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(ammunition_id):
        """Find ammunition by ID"""
        return Ammunition.query.filter_by(id=ammunition_id).first()


class Scope(db.Model):
    """Scope Model - Represents scopes in the system"""
    
    __tablename__ = 'scopes'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    tube_size = Column(String(100), nullable=True)
    focal_plane = Column(String(100), nullable=True)
    reticle = Column(String(255), nullable=True)
    tracking_units = Column(String(100), nullable=True)
    click_value = Column(String(100), nullable=True)
    
    # Total travel information (stored as JSON)
    total_travel = Column(JSON, nullable=True)
    
    # Zero data (stored as JSON array)
    zero_data = Column(JSON, nullable=True, default=list)
    
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, manufacturer, model, **kwargs):
        self.user_id = user_id
        self.manufacturer = manufacturer
        self.model = model
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert scope to dictionary for JSON response"""
        return {
            'id': self.id,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'tubeSize': self.tube_size,
            'focalPlane': self.focal_plane,
            'reticle': self.reticle,
            'trackingUnits': self.tracking_units,
            'clickValue': self.click_value,
            'totalTravel': self.total_travel,
            'zeroData': self.zero_data or [],
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def save(self):
        """Save scope to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete scope from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all scopes by user ID"""
        return Scope.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_id(scope_id):
        """Find scope by ID"""
        return Scope.query.filter_by(id=scope_id).first()


class Maintenance(db.Model):
    """Maintenance Model - Represents maintenance tasks in the system"""
    
    __tablename__ = 'maintenance'
    
    # Primary fields
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    rifle_id = Column(String(36), ForeignKey('rifles.id'), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    
    # Interval information (stored as JSON)
    interval = Column(JSON, nullable=False)
    
    last_completed = Column(DateTime, nullable=True)
    current_count = Column(Integer, nullable=True, default=0)
    torque_spec = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    rifle = db.relationship('Rifle', backref=db.backref('maintenance_tasks', lazy=True))
    
    def __init__(self, user_id, rifle_id, title, type, interval, **kwargs):
        self.user_id = user_id
        self.rifle_id = rifle_id
        self.title = title
        self.type = type
        self.interval = interval
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert maintenance to dictionary for JSON response"""
        return {
            'id': self.id,
            'rifleId': self.rifle_id,
            'title': self.title,
            'type': self.type,
            'interval': self.interval,
            'lastCompleted': self.last_completed.isoformat() if self.last_completed else None,
            'currentCount': self.current_count,
            'torqueSpec': self.torque_spec,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def complete_maintenance(self):
        """Mark maintenance as completed"""
        self.last_completed = datetime.utcnow()
        self.current_count = 0
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save maintenance to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete maintenance from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def find_by_user_id(user_id):
        """Find all maintenance tasks by user ID"""
        return Maintenance.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def find_by_rifle_id(rifle_id):
        """Find all maintenance tasks by rifle ID"""
        return Maintenance.query.filter_by(rifle_id=rifle_id).all()
    
    @staticmethod
    def find_by_id(maintenance_id):
        """Find maintenance by ID"""
        return Maintenance.query.filter_by(id=maintenance_id).first()