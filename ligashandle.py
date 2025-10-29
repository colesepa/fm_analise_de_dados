from pathlib import Path
import json
from typing import Any, Dict, List, Optional
from unidecode import unidecode

class LigasHandler():
    def __init__(self, path: Path) -> None:
        
        self.path = path
        self.data: Dict[str, Any] = self._load()
        

        
    def _load(self) -> Dict[str, Any]:
        
        if not self.path.exists():
            return {"ligas":[]}
        
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _save(self) -> None:
        
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def _att_data(self) -> None:
        self.data = self._load()
    
    def show(self) -> None:
        print(self.data)
       
    def show_json(self) -> None:
        print(json.dumps(self.data, ensure_ascii=False, indent=2))
        
    def get_data(self) -> Dict[str, Any]:
        return self.data
    
    def get_ligas(self, order: bool = True) -> List[Any]:
        
        if len(self.data['ligas']) == 0:
           return []
       
        else:
            ligas = list(set([liga['nome'] for liga in self.data['ligas']]))

            if order:
                ligas = sorted(ligas, key=str.casefold)
        
        return ligas
    
    def get_tier(self, liga:str) -> int | None :
        
        if liga not in self.get_ligas():
            
            print(f"{liga} Não encontrada na base de dados.")
            raise KeyError
        else:
            for x in self.data["ligas"]:
                if unidecode(liga).lower() == unidecode(x["nome"]).lower():
                    return int(x["tier"])
    
    def get_coeficiente(self, liga:str) -> int | None :
        
        if liga not in self.get_ligas():
            
            print(f"{liga} Não encontrada na base de dados.")
            raise KeyError
        else:
            for x in self.data["ligas"]:
                if unidecode(liga).lower() == unidecode(x["nome"]).lower():
                    return int(x["coeficiente"])
    
    def clear(self) -> None:
        
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"ligas":[]}, f, ensure_ascii=False, indent=4) 
        
        self._att_data()
        
    def append(self, 
               nome:str, 
               pais:str,
               tier:str,
               reputacao:str,
               coeficiente:float=1.00) -> None:
       
        liga = {"nome": unidecode(nome),
               "pais": unidecode(pais),
               "tier": int(tier),
               "reputacao": int(reputacao),
               "coeficiente": float(coeficiente)}     
        
        
        for l in self.data["ligas"]:
            if l["nome"].lower() == liga["nome"].lower() and l["pais"].lower() == liga["pais"].lower():
                return
        
        self.data["ligas"].append(liga)
        self._save()
        self._att_data()
        
    def __len__(self) -> int:
        return len(self.data.get("ligas",[]))
    

