# https://stackoverflow.com/questions/59433403/how-to-save-fragment-shader-image-changes-to-image-output-file

# # Requirements # #
# Execute these commands on PyCharm terminal:
# pip install glfw
# pip install pyopengl
# pip install pyrr
# pip install pillow


"""
    The OpenGL specification doesn't allow you to create a context without a window,
    since it needs the pixel format that you set into the device context.
    Actually, it is necessary to have a window handler to create a "traditional" rendering context.
    It is used to fetch OpenGL information and extensions availability.
    Once you got that information, you can destroy the render context and release the "dummy" window.
    So, in this code, the window is created, the context is set to this window,
    the image result is saved to an output image file and, then, this window is released.
"""


import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from PIL import Image


def main():
    # Initialize glfw
    if not glfw.init():
        return

    # Create window
    window = glfw.create_window(1, 1, "My OpenGL window", None, None)  # Size (1, 1) for show nothing in window
    # window = glfw.create_window(800, 600, "My OpenGL window", None, None)

    # Terminate if any issue
    if not window:
        glfw.terminate()
        return

    # Set context to window
    glfw.make_context_current(window)

    #

    # Initial data
    # Positions, colors, texture coordinates
    '''
    #           positions        colors          texture coords
    quad = [   -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
                0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
                0.5,  0.5, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
               -0.5,  0.5, 0.0,  1.0, 1.0, 1.0,  0.0, 1.0]
    '''
    #       positions      colors       texture coords
    quad = [-1., -1., 0.,  1., 0., 0.,  0., 0.,
             1., -1., 0.,  0., 1., 0.,  1., 0.,
             1.,  1., 0.,  0., 0., 1.,  1., 1.,
            -1.,  1., 0.,  1., 1., 1.,  0., 1.]
    quad = numpy.array(quad, dtype=numpy.float32)
    # Vertices indices order
    indices = [0, 1, 2,
               2, 3, 0]
    indices = numpy.array(indices, dtype=numpy.uint32)

    # print(quad.itemsize * len(quad))
    # print(indices.itemsize * len(indices))
    # print(quad.itemsize * 8)

    #

    # Vertex shader
    # vertex_shader = """
    # #version 330

    # in layout(location = 0) vec3 position;

    # //in layout(location = 1) vec3 inColor;
    # //out vec3 outColor;

    # in layout(location = 2) vec2 inTexCoords;
    # out vec2 outTexCoords;

    # void main()
    # {
    #     gl_Position = vec4(position, 1.0f);

    #     //outColor = inColor;

    #     outTexCoords = inTexCoords;
    # }
    # """

    vertex_shader = open("vertex_shader.glsl", "r").read()

    # Fragment shader
    # fragment_shader = """
    # #version 330

    # //in vec3 outColor;

    # //out vec4 gl_FragColor;
    # uniform sampler2D source;
    # in vec2 outTexCoords;

    # float intensityFactor = 2.;

    # void main()
    # {
    #     ivec2 textureSize2d = textureSize(source, 0); // Width and height of texture image

    #     vec3 color = vec3(texture(source, outTexCoords).rgb);
    #     float g = dot(color, vec3(0.299, 0.587, 0.114));

    #     //gl_FragColor = texture(source, outTexCoords) * vec4(1.0f, 0.0f, 1.0f, 1.0f);
    #     gl_FragColor = vec4(mix(color, vec3(g), 1.0f), 1.0f);
    # }
    # """

    fragment_shader = open("shaders/red.glsl","r").read()

    #

    # Compile shaders
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # VBO
    v_b_o = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, v_b_o)
    glBufferData(GL_ARRAY_BUFFER, quad.itemsize * len(quad), quad, GL_STATIC_DRAW)

    # EBO
    e_b_o = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, e_b_o)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    # Configure positions of initial data
    # position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Configure colors of initial data
    # color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # Configure texture coordinates of initial data
    # texture_coords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, quad.itemsize * 8, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    # Texture
    texture = glGenTextures(1)
    # Bind texture
    glBindTexture(GL_TEXTURE_2D, texture)
    # Texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #

    # Open image
    image = Image.open("res/img.png")
    #
    # img_data = numpy.array(list(image.getdata()), numpy.uint8)
    #
    # flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # img_data = flipped_image.convert("RGBA").tobytes()
    #
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    # print(image.width, image.height)

    #

    # Create render buffer with size (image.width x image.height)
    rb_obj = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, rb_obj)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, image.width, image.height)

    # Create frame buffer
    fb_obj = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fb_obj)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, rb_obj)

    # Check frame buffer (that simple buffer should not be an issue)
    status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
    if status != GL_FRAMEBUFFER_COMPLETE:
        print("incomplete framebuffer object")

    #

    # Install program
    glUseProgram(shader)

    # Bind framebuffer and set viewport size
    glBindFramebuffer(GL_FRAMEBUFFER, fb_obj)
    glViewport(0, 0, image.width, image.height)

    # Draw the quad which covers the entire viewport
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    #

    # PNG
    # Read the data and create the image
    image_buffer = glReadPixels(0, 0, image.width, image.height, GL_RGBA, GL_UNSIGNED_BYTE)
    image_out = numpy.frombuffer(image_buffer, dtype=numpy.uint8)
    image_out = image_out.reshape(image.height, image.width, 4)
    img = Image.fromarray(image_out, 'RGBA')
    img.save(r"res/image_out.png")

    # JPG
    '''
    # Read the data and create the image
    image_buffer = glReadPixels(0, 0, image.width, image.height, GL_RGB, GL_UNSIGNED_BYTE)
    image_out = numpy.frombuffer(image_buffer, dtype=numpy.uint8)
    image_out = image_out.reshape(image.height, image.width, 3)
    img = Image.fromarray(image_out, 'RGB')
    img.save(r"res/image_out.jpg")
    '''

    #

    # Bind default frame buffer (0)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    # Set viewport rectangle to window size
    glViewport(0, 0, 0, 0)  # Size (0, 0) for show nothing in window
    # glViewport(0, 0, 800, 600)

    # Set clear color
    glClearColor(0., 0., 0., 1.)

    #

    # Program loop
    while not glfw.window_should_close(window):
        # Call events
        glfw.poll_events()

        # Clear window
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        # Send to window
        glfw.swap_buffers(window)

        # Force terminate program, since it will work like clicked in 'Close' button
        break

    #

    # Terminate program
    glfw.terminate()


if __name__ == "__main__":
    main()