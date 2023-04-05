import os
import uuid
from flask import Blueprint, render_template, flash, redirect, request, url_for, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required, roles_accepted
from ..models import db
from .proveedores import insertar_proveedor, modificar_proveedor_get, modificar_proveedor_post
from project.models import Products, Role, Proveedor
from werkzeug.utils import secure_filename
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

administrador = Blueprint('administrador', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


# Definimos la ruta para la página de perfil de usuairo


@administrador.route('/administrador')
@login_required
@roles_required('admin')
def admin():
    productos = Products.query.all()
    return render_template('RopaCrud.html', productos=productos)


@administrador.route('/administrador', methods=['POST'])
@login_required
@roles_required('admin')
def admin_post():
    img=str(uuid.uuid4())+'.png'
    imagen=request.files['image']
    ruta_imagen = os.path.abspath('project\\static\\img')
    imagen.save(os.path.join(ruta_imagen,img))       
    alum=Products(nombre=request.form.get('txtNombre'),
                    descripcion=request.form.get('txtDescripcion'),
                    estilo=request.form.get('txtEstilo'),
                    precio=request.form.get('txtPrecio'),
                    image=img)
        #Con esta instruccion guardamos los datos en la bd
    db.session.add(alum)
    db.session.commit()
    flash("El registro se ha guardado exitosamente.", "exito")
    return redirect(url_for('main.principalAd'))
    

@administrador.route('/modificar', methods=['GET', 'POST'])
@login_required
def modificar():
    if request.method == 'GET':
        id = request.args.get('id')
        producto = Products.query.get(id)
        print(producto)
        if producto is None:
            flash("El pzroducto no existe", "error")
            return redirect(url_for('administrador.admin'))
        if not producto.image:
            producto.image = 'default.png' # o cualquier otro valor predeterminado para la imagen
        return render_template('modificar.html', producto=producto,id=id)
    elif request.method == 'POST':
        id = request.args.get('id')
        producto = Products.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe", "error")
            return redirect(url_for('administrador.admin'))
        producto.nombre = request.form.get('txtNombre')
        producto.estilo = request.form.get('txtEstilo')
        producto.descripcion = request.form.get('txtDescripcion')
        producto.precio = request.form.get('txtPrecio')
        imagen = request.files.get('image')
        ruta_imagen = os.path.abspath('project\\static\\img')
        if imagen:
            # Eliminar la imagen anterior
            os.remove(os.path.join(ruta_imagen, producto.image))
            # Guardar la nueva imagen
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            producto.image = filename
        db.session.commit()
        flash("El registro se ha modificado exitosamente.", "exito")
        return redirect(url_for('main.principalAd'))

@administrador.route('/eliminar', methods=['GET', 'POST'])
@login_required
def eliminar():
    if request.method == 'GET':
        id = request.args.get('id')
        producto = Products.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe", "error")
            return redirect(url_for('administrador.admin'))
        if not producto.image:
            producto.image = 'default.png' # o cualquier otro valor predeterminado para la imagen
        return render_template('eliminar.html', producto=producto,id=id)
    elif request.method == 'POST':
        id = request.args.get('id')
        producto = Products.query.get(id)
        print(producto)
        if producto is None:
            flash("El producto no existe", "error")
            return redirect(url_for('administrador.admin'))
        producto.nombre = request.form.get('txtNombre')
        producto.estilo = request.form.get('txtEstilo')
        producto.descripcion = request.form.get('txtDescripcion')
        producto.precio = request.form.get('txtPrecio')
        imagen = request.files.get('image')
        ruta_imagen = os.path.abspath('project\\static\\img')
        if imagen:
            # Eliminar la imagen anterior
            os.remove(os.path.join(ruta_imagen, producto.image))
            # Guardar la nueva imagen
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(ruta_imagen, filename))
            producto.image = filename
        db.session.delete(producto)
        db.session.commit()
        flash("El registro se ha eliminado exitosamente.", "exito")
        return redirect(url_for('main.principalAd'))
    
@administrador.route('/proveedores', methods=['GET'])
@login_required
def proveedores():   
    proveedores = Proveedor.query.filter_by(active=1).all()
    return render_template('proveedores.html', proveedores=proveedores)

@administrador.route('/insertar_prov', methods=['GET','POST'])
@login_required
def proveedores_insertar():
    if request.method == 'POST':
       return insertar_proveedor()
    return render_template('insertar_proveedor.html')

@administrador.route('/modificar_prov', methods=['GET','POST'])
@login_required
def modificar_prov():
    if request.method == 'GET':
        return modificar_proveedor_get()
    elif request.method == 'POST':
       return modificar_proveedor_post()
    