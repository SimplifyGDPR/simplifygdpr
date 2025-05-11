from fastapi import APIRouter

router = APIRouter(
    prefix="/clausula",
    tags=["Cláusulas legales"]
)

@router.get("/aviso")
def generar_aviso_legal():
    return {
        "titulo": "Aviso Legal",
        "contenido": (
            "En cumplimiento con el deber de información recogido en el artículo 10 de la Ley 34/2002, "
            "de 11 de julio, de Servicios de la Sociedad de la Información y del Comercio Electrónico, "
            "se informa que este sitio web es propiedad de SimplifyGDPR."
        )
    }
