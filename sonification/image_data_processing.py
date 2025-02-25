import cv2 as cv
import numpy as np
from sonification.sonification import tuples_to_midi
from sonification.SonificationConfig import SonificationConfig
import matplotlib.pyplot as plt

def image_to_midi(image, config: SonificationConfig):
    cell_image_buffer = []
    bbox_color = (214, 122, 144)
    bbox_thickness = 3
    
    height, width, _ = image.shape
    aspect_ratio = height / width
    new_width = (1080 // config.grid_cols) * config.grid_cols #every image will become ~1080px wide
    new_height = (int(new_width * aspect_ratio) // config.grid_rows) * config.grid_rows

    # resize image to line up with grid perfectly
    image = cv.resize(image, (new_width + bbox_thickness, new_height + bbox_thickness))
    grid_image = image.copy()

    cell_width = new_width // config.grid_cols
    cell_height = new_height // config.grid_rows
    
    note_tuples = []
    
    # draw default grid
    if config.render_grid:
        for y in range(0, new_height + 1, cell_height):
            cv.line(grid_image, (0, y), (new_width, y), bbox_color, bbox_thickness)
        for x in range(0, new_width + 1, cell_width):
            cv.line(grid_image, (x, 0), (x, new_height), bbox_color, bbox_thickness)
        
    cell_image_buffer.append(grid_image)

    for row in range(config.grid_rows):
        for col in range(config.grid_cols):
            # calculate the bounding box for each grid cell
            y_start = row * cell_height
            y_end = y_start + cell_height
            x_start = col * cell_width
            x_end = x_start + cell_width
            
            # crop the cell 
            cell = image[y_start:y_end, x_start:x_end]
            
            #generate selected cell image
            selected_cell_image = generate_selected_cell_image(grid_image, y_start, y_end, x_start, x_end, bbox_thickness)
            cell_image_buffer.append(selected_cell_image)

            # cell based processing
            if(config.process_rgb):
                blue_channel = cell[:, :, 0]
                green_channel = cell[:, :, 1]
                red_channel = cell[:, :, 2]

                # avg brightness for each channel
                avg_blue = np.mean(blue_channel)
                avg_green = np.mean(green_channel)
                avg_red = np.mean(red_channel)

                current_pos = len(note_tuples)/3
                note_tuples.append((current_pos,round(avg_blue)))
                note_tuples.append((current_pos,round(avg_green)))
                note_tuples.append((current_pos,round(avg_red)))
            else:
                avg_brightness = np.mean(cv.cvtColor(cell, cv.COLOR_BGR2GRAY))
                # print(f"cell ({row}, {col}) avg brightness: {avg_brightness}")
                note_tuples.append((len(note_tuples), round(avg_brightness)))
                
    result_midi, pitch_mapped_data = tuples_to_midi(note_tuples, config)
    plot_image_buffer = generate_selected_cell_plot(pitch_mapped_data)
    return result_midi, plot_image_buffer, cell_image_buffer

def generate_selected_cell_image(grid_image, y_start, y_end, x_start, x_end, bbox_thickness, overlay_color=(214, 122, 144), overlay_alpha=0.8):
    selected_cell_image = grid_image.copy()

    cell = selected_cell_image[y_start:y_end+bbox_thickness, x_start:x_end+bbox_thickness]
    overlay = np.full(cell.shape, overlay_color, dtype=np.uint8)
    
    cv.addWeighted(overlay, overlay_alpha, cell, 1 - overlay_alpha, 0, cell)
    
    # Return the modified image with the overlay applied to the specified cell
    selected_cell_image[y_start:y_end+bbox_thickness, x_start:x_end+bbox_thickness] = cell
    return selected_cell_image

def generate_selected_cell_plot(pitch_mapped_data):
    plot_image_buffer = []
    data_extended = np.insert(pitch_mapped_data, 0, pitch_mapped_data[0])  # Repeat the first element
    x = np.arange(len(data_extended))
    fig, ax = plt.subplots(figsize=(5, 1))
    
    ax.set_facecolor('#0E1117')
    fig.patch.set_alpha(0)
    
    ax.step(x, data_extended, color='#907ad6')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)

    fig.patch.set_visible(False)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.canvas.draw()
    
    # blank graph for default image
    plot_image = cv.cvtColor(np.array(fig.canvas.renderer.buffer_rgba()), cv.COLOR_RGBA2BGR)
    plot_image = plot_image[0:100, 22:478] # crop the image to remove padding
    plot_image_buffer.append(plot_image)
    

    for i in range(1, len(data_extended)):
        line = ax.axvline(i-0.5, color='#907ad6')

        fig.canvas.draw()
        plot_image = cv.cvtColor(np.array(fig.canvas.renderer.buffer_rgba()), cv.COLOR_RGBA2BGR)
        plot_image = plot_image[0:100, 22:478]
        plot_image_buffer.append(plot_image)

        line.remove()
    plt.close(fig)

    return plot_image_buffer