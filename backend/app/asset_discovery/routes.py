from flask import Blueprint, request, jsonify

from app.asset_discovery.services import (
    AssetDiscoveryService
)


discovery_bp = Blueprint(
    "asset_discovery",
    __name__
)


@discovery_bp.route(
    "/scan",
    methods=["POST"]
)
def scan_asset():

    data = request.get_json()


    target = data.get("target")

    port = data.get(
        "port",
        443
    )


    if not target:

        return jsonify({

            "success": False,
            "message": "Target required"

        }),400



    try:

        asset = (
            AssetDiscoveryService
            .scan_asset(
                target,
                port
            )
        )


        return jsonify({

            "success": True,

            "message":
            "Asset discovered",

            "asset":
            asset.to_dict()

        }),200



    except Exception as e:

        return jsonify({

            "success":False,

            "error":str(e)

        }),500





@discovery_bp.route(
    "",
    methods=["GET"]
)
def get_assets():


    assets = (
        AssetDiscoveryService
        .get_assets()
    )


    return jsonify([

        asset.to_dict()

        for asset in assets

    ])





@discovery_bp.route(
    "/<int:id>",
    methods=["GET"]
)
def get_asset(id):


    asset = (
        AssetDiscoveryService
        .get_asset(id)
    )


    return jsonify(
        asset.to_dict()
    )





@discovery_bp.route(
    "/<int:id>",
    methods=["DELETE"]
)
def delete_asset(id):


    AssetDiscoveryService.delete_asset(
        id
    )


    return jsonify({

        "success":True,

        "message":
        "Asset deleted"

    })





@discovery_bp.route(
    "/<int:id>/rescan",
    methods=["POST"]
)
def rescan_asset(id):


    asset = (
        AssetDiscoveryService
        .rescan(id)
    )


    return jsonify(
        asset.to_dict()
    )
