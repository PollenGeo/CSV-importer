import ezomero
from ezomero.rois import Rectangle
from omero.gateway import BlitzGateway
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


def connect(hostname, username, password):
    """
    Connect to the OMERO server.
    """
    conn = BlitzGateway(username, password, host=hostname, port=4064, secure=True)
    if not conn.connect():
        raise ConnectionError("Failed to connect to the OMERO server")
    conn.c.enableKeepAlive(60)
    return conn


def list_groups(conn):
    """
    Retrieves a list of all available groups in OMERO and returns a dictionary {ID: Name}.
    """
    groups = conn.getGroupsMemberOf()
    group_dict = {g.getId(): g.getName() for g in groups}

    # Build a string to display available groups
    group_list_str = "\n".join([f"ID: {g_id} - {name}" for g_id, name in group_dict.items()])
    return group_dict, group_list_str


def change_omero_group(conn, group_id):
    """
    Changes to the specified group by ID.
    """
    conn.setGroupForSession(group_id)
    print(f"Successfully switched to group with ID {group_id}.")


def add_rois_from_csv(conn, csv_path):
    """
    Reads a CSV file and adds rectangular ROIs to OMERO, visible across all Z layers.
    """
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        image_id = int(row["image_id"])
        roi_type = row["type"].strip().lower()

        if roi_type == "rectangle":
            x = int(row["X"])
            y = int(row["Y"])
            width = int(row["Width"])
            height = int(row["Height"])

            # Create rectangle across all Z layers
            rect = Rectangle(
                x=x, y=y, width=width, height=height, z=None,  # <- Visible across all Z layers
                label=f"Rectangle {row['segment_id']}"
            )

            # Add ROI to the image in OMERO
            try:
                ezomero.post_roi(conn, image_id, [rect])
                print(f"ROI added to image {image_id}: Rect({x}, {y}, {width}, {height}) across all Z layers")
            except Exception as e:
                print(f"Error adding ROI to image {image_id}: {e}")

    messagebox.showinfo("Success", "ROIs successfully added across all Z layers.")


def main():
    root = tk.Tk()
    root.withdraw()

    conn = None

    try:
        # Request OMERO credentials
        hostname = simpledialog.askstring("Host", "Host:", initialvalue="xxx") #Put your initial host
        username = simpledialog.askstring("Username", "Username:")
        password = simpledialog.askstring("Password", "Password:", show='*')

        if not all([hostname, username, password]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = connect(hostname, username, password)

        # Get the list of available groups
        group_dict, group_list_str = list_groups(conn)

        # Show the list of groups to the user and request an ID input
        selected_group_id = simpledialog.askinteger(
            "Select Group",
            f"Available groups:\n{group_list_str}\n\nEnter the ID of the group you want to switch to:"
        )

        # Verify if the entered group ID is valid
        if selected_group_id not in group_dict:
            messagebox.showerror("Error", "Invalid group ID. Please try again.")
            return

        # Switch to the selected group
        change_omero_group(conn, selected_group_id)

        # Show required CSV columns before file selection
        required_columns = "The CSV file must contain the following columns:\n\n" \
                           "- image_id\n" \
                           "- type ('rectangle')\n" \
                           "- X \n" \
                           "- Y \n" \
                           "- Width \n" \
                           "- Height \n" \
                           "- segment_id \n\n" \
                           "Ensure your CSV file is formatted correctly before proceeding."

        messagebox.showinfo("CSV Requirements", required_columns)

        # Allow the user to select the CSV file
        csv_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

        if not csv_path:
            messagebox.showwarning("Input Error", "A CSV file must be selected.")
            return

        # Add the ROIs to the image in OMERO
        add_rois_from_csv(conn, csv_path)

        messagebox.showinfo("Success", "ROIs successfully added across all Z layers.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
