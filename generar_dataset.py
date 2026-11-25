import json 
import subprocess

from datetime import datetime
from zoneinfo import ZoneInfo

DATASET_FILE = "datos.json"

DATASET_VERSION = 1

COMBUSTIBLES = {
    18: "GNC",
    31: "BGNC"
}

URL_BASE = (
    "https://sedeaplicaciones.minetur.gob.es/"
    "ServiciosRESTCarburantes/"
    "PreciosCarburantes/"
    "EstacionesTerrestres/"
    "FiltroProducto/{}"
)

LIMPIEZA_DIAS = 90

MADRID_TZ = ZoneInfo(
    "Europe/Madrid"
)

HOY = datetime.now(
    MADRID_TZ
).date()


def fecha_actual():

    return datetime.now(
        MADRID_TZ
    ).strftime(
        "%Y-%m-%d %H:%M"
    )


def parse_precio(valor):
    """
    Reglas de negocio:

    null  -> 0.0
    ""    -> 0.0
    "0"   -> 0.0
    error -> 0.0
    """

    if valor is None:
        return 0.0

    valor = str(valor).strip()

    if valor == "":
        return 0.0

    try:

        return float(
            valor.replace(",", ".")
        )

    except Exception:

        return 0.0


def parse_coordenada(valor):
    """
    Reglas de negocio:

    null -> None
    ""   -> None
    "0"  -> None
    error-> None
    """

    if valor is None:
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    try:

        numero = float(
            valor.replace(",", ".")
        )

        if numero == 0:
            return None

        return numero

    except Exception:

        return None


def texto_valido(valor):

    if valor is None:
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    return valor


def descargar_dataset(
    id_combustible
):

    url = URL_BASE.format(
        id_combustible
    )

    print(
        f"Descargando combustible "
        f"{id_combustible}"
    )

    resultado = subprocess.run(
        [
            "curl",
            "-L",
            url
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return json.loads(
        resultado.stdout
    )


def cargar_dataset_existente():

    try:

        with open(
            DATASET_FILE,
            "r",
            encoding="utf-8"
        ) as fichero:

            return json.load(
                fichero
            )

    except FileNotFoundError:

        print(
            "No existe dataset previo."
        )

        return {

            "version":
                DATASET_VERSION,

            "ultimaGeneracion":
                None,

            "fechaDataset":
                None,

            "numeroEstaciones":
                0,

            "estaciones":
                []
        }


def convertir_a_mapa(
    dataset
):

    mapa = {}

    for estacion in dataset.get(
        "estaciones",
        []
    ):

        estacion_id = estacion.get(
            "id"
        )

        if estacion_id:

            mapa[
                estacion_id
            ] = estacion

    return mapa


def crear_estacion(
    ministerio
):

    estacion = {

        "id":
            ministerio.get(
                "IDEESS"
            ),

        "nombre":
            texto_valido(
                ministerio.get(
                    "Rótulo"
                )
            ),

        "direccion":
            texto_valido(
                ministerio.get(
                    "Dirección"
                )
            ),

        "codigoPostal":
            texto_valido(
                ministerio.get(
                    "C.P."
                )
            ),

        "municipio":
            texto_valido(
                ministerio.get(
                    "Municipio"
                )
            ),

        "provincia":
            texto_valido(
                ministerio.get(
                    "Provincia"
                )
            ),

        "idMunicipio":
            texto_valido(
                ministerio.get(
                    "IDMunicipio"
                )
            ),

        "idProvincia":
            texto_valido(
                ministerio.get(
                    "IDProvincia"
                )
            ),

        "idComunidad":
            texto_valido(
                ministerio.get(
                    "IDCCAA"
                )
            ),

        "horario":
            texto_valido(
                ministerio.get(
                    "Horario"
                )
            ),

        "latitud":
            parse_coordenada(
                ministerio.get(
                    "Latitud"
                )
            ),

        "longitud":
            parse_coordenada(
                ministerio.get(
                    "Longitud (WGS84)"
                )
            ),

        "combustibles":
            {}
    }

    return estacion


def actualizar_texto_si_valido(
    estacion,
    clave,
    valor
):

    if valor is not None:

        estacion[
            clave
        ] = valor


def actualizar_datos_maestros(
    estacion,
    ministerio
):

    actualizar_texto_si_valido(
        estacion,
        "nombre",
        texto_valido(
            ministerio.get(
                "Rótulo"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "direccion",
        texto_valido(
            ministerio.get(
                "Dirección"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "codigoPostal",
        texto_valido(
            ministerio.get(
                "C.P."
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "municipio",
        texto_valido(
            ministerio.get(
                "Municipio"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "provincia",
        texto_valido(
            ministerio.get(
                "Provincia"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "idMunicipio",
        texto_valido(
            ministerio.get(
                "IDMunicipio"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "idProvincia",
        texto_valido(
            ministerio.get(
                "IDProvincia"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "idComunidad",
        texto_valido(
            ministerio.get(
                "IDCCAA"
            )
        )
    )

    actualizar_texto_si_valido(
        estacion,
        "horario",
        texto_valido(
            ministerio.get(
                "Horario"
            )
        )
    )

    latitud = parse_coordenada(
        ministerio.get(
            "Latitud"
        )
    )

    longitud = parse_coordenada(
        ministerio.get(
            "Longitud (WGS84)"
        )
    )

    if latitud is not None:

        estacion[
            "latitud"
        ] = latitud

    if longitud is not None:

        estacion[
            "longitud"
        ] = longitud


def actualizar_combustible(
    estacion,
    id_combustible,
    precio
):

    clave = str(
        id_combustible
    )

    estacion[
        "combustibles"
    ][clave] = {

        "tipo":
            COMBUSTIBLES.get(
                id_combustible,
                str(
                    id_combustible
                )
            ),

        "precio":
            precio,

        "fechaActualizacion":
            fecha_actual()
    }


def procesar_respuesta(
    respuesta,
    id_combustible,
    mapa
):

    for ministerio in respuesta.get(
        "ListaEESSPrecio",
        []
    ):

        ideess = ministerio.get(
            "IDEESS"
        )

        if not ideess:
            continue

        if ideess not in mapa:

            mapa[
                ideess
            ] = crear_estacion(
                ministerio
            )

        estacion = mapa[
            ideess
        ]

        actualizar_datos_maestros(
            estacion,
            ministerio
        )

        precio = parse_precio(
            ministerio.get(
                "PrecioProducto"
            )
        )

        actualizar_combustible(
            estacion,
            id_combustible,
            precio
        )


def limpiar_combustibles(
    mapa
):

    estaciones_a_borrar = []

    for (
        ideess,
        estacion
    ) in mapa.items():

        combustibles = estacion.get(
            "combustibles",
            {}
        )

        combustibles_a_borrar = []

        for (
            clave,
            info
        ) in combustibles.items():

            try:

                fecha = datetime.strptime(
                    info[
                        "fechaActualizacion"
                    ],
                    "%Y-%m-%d %H:%M"
                ).date()

            except Exception:

                combustibles_a_borrar.append(
                    clave
                )

                continue

            dias = (
                HOY - fecha
            ).days

            if dias > LIMPIEZA_DIAS:

                combustibles_a_borrar.append(
                    clave
                )

        for clave in combustibles_a_borrar:

            del combustibles[
                clave
            ]

        if len(
            combustibles
        ) == 0:

            estaciones_a_borrar.append(
                ideess
            )

    for ideess in estaciones_a_borrar:

        print(
            f"Eliminando estación "
            f"{ideess}"
        )

        del mapa[
            ideess
        ]


def guardar_dataset(
    mapa
):

    resultado = {

        "version":
            DATASET_VERSION,

        "ultimaGeneracion":

            datetime.now(
                MADRID_TZ
            ).isoformat(),

        "fechaDataset":

            fecha_actual(),

        "numeroEstaciones":

            len(
                mapa
            ),

        "estaciones":

            sorted(

                mapa.values(),

                key=lambda e: (

                    e.get(
                        "provincia",
                        ""
                    ),

                    e.get(
                        "municipio",
                        ""
                    ),

                    e.get(
                        "nombre",
                        ""
                    )
                )
            )
    }

    with open(
        DATASET_FILE,
        "w",
        encoding="utf-8"
    ) as fichero:

        json.dump(
            resultado,
            fichero,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"Guardadas "
        f"{len(mapa)} estaciones"
    )


def main():

    dataset_existente = (
        cargar_dataset_existente()
    )

    mapa = convertir_a_mapa(
        dataset_existente
    )

    for (
        id_combustible,
        _
    ) in COMBUSTIBLES.items():

        try:

            respuesta = (
                descargar_dataset(
                    id_combustible
                )
            )

            procesar_respuesta(
                respuesta,
                id_combustible,
                mapa
            )

        except Exception as ex:

            print(
                f"Error descargando "
                f"{id_combustible}: "
                f"{ex}"
            )

    limpiar_combustibles(
        mapa
    )

    guardar_dataset(
        mapa
    )


if __name__ == "__main__":

    main()
