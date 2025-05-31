Objetivo: utilizar modelos de lenguaje natural para analizar y consultar información relacionada con temas complejos y controversiales. Para esto se generaron embeddings a partir de documentos, mediante AnythingLLM y el modelo LLaMA3 a través de Ollama.
Para este proyecto comencé buscando artículo de los temas aacordados: 
1.-  “La autonomía personal frente al inicio de la vida: el dilema del aborto en contextos éticos y tecnológicos”.
Al buscar los articulos intenté que fueran lo más neutral posible, que fueran tanto a favor como en contra, para que al hacer las preguntas no tomara una postura más de un lado que de otra.
Después de elegir los artículos fueron guardados con la extensión .pdf para que fuera más fácil que se creen los embeddings.
Se descargó Ollama con el modelo llama3 que funciona de manera local en nuestra computadora y AnythingLLM para cargar los documentos y hacer las preguntas correspondientes a la IA.
Configuré AnythingLLM para poder usarlo en el entorno de ollama, con el modelo llama3 y lo iniciamos.
Creé un workspace con el nombre "Aborto" y se subiendo los documentos antes investigados, seleccioné los documentosa usarse  y automáticamente se crearon los embeddings en base a los documentos, esperé a que se crearán ya que toma su tiempo en crearlos pero una vez creados ya estaba todo listo para hacer las preguntas correspondientes que marcaba la asiganción.
En base a las respuestas que fueron dadas con la IA se puede ver que tiene una postura neutra 