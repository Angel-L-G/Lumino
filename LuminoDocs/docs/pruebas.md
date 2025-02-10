## Pruebas

### Estrategia de pruebas

- Pruebas unitarias en componentes clave.
- Pruebas de integración entre servicios.

### Casos de prueba

Se pueden observar en los ficheros de testing ubicados en: /tests

```python
# Ejemplo
@pytest.mark.django_db
def test_user_detail_displays_all_elements(client, student, teacher):
    client.force_login(student)
    response = client.get(f'/users/{student.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, f'{student.first_name} {student.last_name}')
    assertContains(response, 'Student')
    assertContains(response, student.email)
    assertContains(response, student.profile.bio)
    response_text = response.content.decode()
    # sorl-thumbnail creates this path for thumbnails
    assert re.search(r'<img.*?src="/media/cache.*?"', response_text, re.S | re.M)

    response = client.get(f'/users/{teacher.username}/')
    assert response.status_code == HTTPStatus.OK
    assertContains(response, 'Teacher')
```

En el test se comprueba que los detalles del usuario son mostrados correctamente.

### Cobertura de pruebas

Se utiliza pytest para medir la cobertura y asegurar que el código esté probado.

### Automatización

Se emplean herramientas como baker para generar modelos aleatorios.
