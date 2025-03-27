from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import mean
from modules.state_manager import state_manager

@dataclass
class KudosRating:
    """Représente une notation entre usagers"""
    rater_id: str
    rated_id: str
    score: float
    timestamp: datetime
    comment: Optional[str] = None

class KudosError(Exception):
    """Exception spécifique au système Kudos"""
    pass

@dataclass
class KudosTransaction:
    """Représente une transaction Kudos"""
    sender: str
    receiver: str
    amount: float
    timestamp: datetime
    description: str
    rating: Optional[KudosRating] = None

@dataclass
class KudosAccount:
    """Compte Kudos d'un usager"""
    user_id: str
    balance: float
    monthly_limit: float
    last_update: datetime
    transactions: List[KudosTransaction]
    ratings: List[KudosRating]
    reputation_score: float

    def add_transaction(self, transaction: KudosTransaction) -> None:
        """Ajoute une transaction au compte"""
        self.transactions.append(transaction)
        self.balance += transaction.amount
        self.last_update = transaction.timestamp

    def validate_transaction(self, amount: float) -> bool:
        """Valide une transaction"""
        if self.balance < amount:
            return False
        if self.balance + amount > self.monthly_limit:
            return False
        return True

    def add_rating(self, rating: KudosRating) -> None:
        """Ajoute une notation et met à jour le score de réputation"""
        self.ratings.append(rating)
        self.update_reputation_score()

    def update_reputation_score(self) -> None:
        """Met à jour le score de réputation"""
        if not self.ratings:
            self.reputation_score = 3.0  # Score par défaut
            return

        # Calculer la moyenne des notes des 6 derniers mois
        recent_ratings = [
            r for r in self.ratings
            if r.timestamp > datetime.now() - timedelta(days=180)
        ]
        
        if recent_ratings:
            scores = [r.score for r in recent_ratings]
            self.reputation_score = mean(scores)
        else:
            self.reputation_score = 3.0

class KudosSystem:
    """Système de gestion des Kudos"""
    
    def __init__(self):
        self.accounts: Dict[str, KudosAccount] = {}
        self.kudos_value = state_manager.get('kudos_value', 1.0)  # 1 Kudo = 1 kWh
        self.monthly_limit = state_manager.get('kudos_monthly_limit', 5000.0)
        self.expiration_months = state_manager.get('kudos_expiration_months', 12)
        self.min_rating = state_manager.get('kudos_notation_min', 3.0)
        
    def create_account(self, user_id: str) -> None:
        """Crée un compte Kudos pour un usager"""
        if user_id in self.accounts:
            raise KudosError(f"Compte déjà existant pour l'usager {user_id}")
        
        self.accounts[user_id] = KudosAccount(
            user_id=user_id,
            balance=0.0,
            monthly_limit=self.monthly_limit,
            last_update=datetime.now(),
            transactions=[],
            ratings=[],
            reputation_score=3.0  # Score initial
        )
    
    def add_kudos(self, user_id: str, amount: float, description: str = "Production d'énergie") -> None:
        """Ajoute des Kudos à un compte"""
        if user_id not in self.accounts:
            self.create_account(user_id)
        
        account = self.accounts[user_id]
        if not account.validate_transaction(amount):
            raise KudosError("Transaction invalide: dépassement du plafond mensuel")
            
        transaction = KudosTransaction(
            sender="SYSTEM",
            receiver=user_id,
            amount=amount,
            timestamp=datetime.now(),
            description=description
        )
        
        account.add_transaction(transaction)
        
    def use_kudos(self, sender_id: str, receiver_id: str, amount: float, description: str = "Échange d'énergie") -> KudosTransaction:
        """Utilise des Kudos pour un échange d'énergie"""
        if sender_id not in self.accounts:
            raise KudosError(f"Compte source non trouvé: {sender_id}")
        if receiver_id not in self.accounts:
            raise KudosError(f"Compte destination non trouvé: {receiver_id}")
        
        sender_account = self.accounts[sender_id]
        receiver_account = self.accounts[receiver_id]
        
        if not sender_account.validate_transaction(-amount):
            raise KudosError("Solde insuffisant")
            
        # Créer la transaction
        transaction = KudosTransaction(
            sender=sender_id,
            receiver=receiver_id,
            amount=amount,
            timestamp=datetime.now(),
            description=description
        )
        
        # Mettre à jour les comptes
        sender_account.add_transaction(transaction)
        receiver_account.add_transaction(transaction)
        
        return transaction
    
    def add_rating(self, rater_id: str, rated_id: str, score: float, comment: Optional[str] = None) -> None:
        """Ajoute une notation entre usagers"""
        if rater_id not in self.accounts:
            raise KudosError(f"Compte évaluateur non trouvé: {rater_id}")
        if rated_id not in self.accounts:
            raise KudosError(f"Compte évalué non trouvé: {rated_id}")
        
        if not (0 <= score <= 5):
            raise KudosError("Score invalide: doit être entre 0 et 5")
        
        rating = KudosRating(
            rater_id=rater_id,
            rated_id=rated_id,
            score=score,
            timestamp=datetime.now(),
            comment=comment
        )
        
        self.accounts[rated_id].add_rating(rating)
    
    def get_balance(self, user_id: str) -> float:
        """Obtient le solde Kudos d'un usager"""
        if user_id not in self.accounts:
            raise KudosError(f"Compte non trouvé: {user_id}")
        return self.accounts[user_id].balance
    
    def get_reputation_score(self, user_id: str) -> float:
        """Obtient le score de réputation d'un usager"""
        if user_id not in self.accounts:
            raise KudosError(f"Compte non trouvé: {user_id}")
        return self.accounts[user_id].reputation_score
    
    def get_transactions(self, user_id: str) -> List[KudosTransaction]:
        """Obtient l'historique des transactions d'un usager"""
        if user_id not in self.accounts:
            raise KudosError(f"Compte non trouvé: {user_id}")
        return self.accounts[user_id].transactions
    
    def get_ratings(self, user_id: str) -> List[KudosRating]:
        """Obtient l'historique des notations reçues par un usager"""
        if user_id not in self.accounts:
            raise KudosError(f"Compte non trouvé: {user_id}")
        return self.accounts[user_id].ratings
    
    def cleanup_expired(self) -> None:
        """Supprime les Kudos et notations expirés"""
        current_time = datetime.now()
        for account in self.accounts.values():
            # Supprimer les transactions expirées
            account.transactions = [
                t for t in account.transactions
                if t.timestamp + timedelta(months=self.expiration_months) > current_time
            ]
            
            # Supprimer les notations anciennes (plus de 6 mois)
            account.ratings = [
                r for r in account.ratings
                if r.timestamp > current_time - timedelta(days=180)
            ]
            
            # Recalculer le solde et le score de réputation
            account.balance = sum(t.amount for t in account.transactions)
            account.update_reputation_score()

# Instance unique du système Kudos
kudos_system = KudosSystem()
