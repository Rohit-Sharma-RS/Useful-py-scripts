import os
import platform


def hide_folder(folder_path):
    """Hides the specified folder based on the operating system."""
    if platform.system() == "Windows":
        os.system(f'attrib +h "{folder_path}"')
        print(f"Folder '{folder_path}' is now hidden.")
    else:
        folder_dir, folder_name = os.path.split(folder_path)
        hidden_folder = os.path.join(folder_dir, f".{folder_name}")
        os.rename(folder_path, hidden_folder)
        print(f"Folder renamed to '{hidden_folder}' to hide it.")

def unhide_folder(folder_path):
    """Unhides the specified folder based on the operating system."""
    if platform.system() == "Windows":
        os.system(f'attrib -h "{folder_path}"')
        print(f"Folder '{folder_path}' is now visible.")
    else:
        folder_dir, folder_name = os.path.split(folder_path)
        if folder_name.startswith("."):
            visible_folder = os.path.join(folder_dir, folder_name[1:])
            os.rename(folder_path, visible_folder)
            print(f"Folder renamed to '{visible_folder}' to unhide it.")
        else:
            print(f"Folder '{folder_path}' is already visible.")

def main():
    print("Folder Hider/Unhider")
    folder_path = input("Enter the full path of the folder: ").strip()

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    action = input("Do you want to (H)ide or (U)nhide the folder? ").lower()
    if action == "h":
        hide_folder(folder_path)
    elif action == "u":
        unhide_folder(folder_path)
    else:
        print("Invalid option. Please choose 'H' to hide or 'U' to unhide.")

if __name__ == "__main__":
    main()
