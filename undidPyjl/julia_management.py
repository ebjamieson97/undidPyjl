from juliacall import Main as jl

# Checks if the Undid.jl Julia package is installed and reports the currently installed version. 
# If it is not installed, installs the most recent version from https://github.com/ebjamieson97/Undid.jl
def checkundidversion():
    """
    Check the version of Undid.jl currently installed in Julia.
    If it is not installed, installs the most recent version from https://github.com/ebjamieson97/Undid.jl
    """

    jl.seval("""
    using Pkg
    deps = Pkg.dependencies()  
    try 
        global package_version = deps[Base.UUID("b4918ae7-7c73-4176-80be-8405760cf2ee")].version  # Declare as local
    catch e
        println("Undid.jl package not found in the current environment.")
        println("Installing Undid.jl now.")
        Pkg.add(url="https://github.com/ebjamieson97/Undid.jl")
        println("Undid.jl is done installing.")
        global deps = Pkg.dependencies()
        global package_version = deps[Base.UUID("b4918ae7-7c73-4176-80be-8405760cf2ee")].version  # Declare as local
    end
    """)
  
    current_Undid_version = jl.seval("package_version")  


    jl.seval("""
   
    url = "https://raw.githubusercontent.com/ebjamieson97/Undid.jl/main/Project.toml"
             
    using Downloads
             
    try
        local content = Downloads.download(url)
        local file_content = read(content, String)
        local start_pos = findfirst("version = ", file_content)
        local start = start_pos[end]
        global newest_version = file_content[start+2:start+7]
    catch e
        println("An error occurred: ", e)
        global newest_version = "Unable to fetch latest version of Undid.jl. Please check your internet connection and try again."
    end
    
    """)  

    newest_version = jl.seval("newest_version")
    newest_version = newest_version.replace('"', '') 

    print(f"Currently installed version of Undid.jl is: {current_Undid_version} \nLatest version of Undid.jl is: {newest_version} \nConsider running command `updateundid()` if installed version is out of date.")

# Updates Undid.jl to the latest version
def updateundid():
    """
    Updates Undid.jl to the latest version.
    This may take a minute or so depending on network and system conditions.
    """
    jl.seval("""
    using Pkg
    try 
        Pkg.rm("Undid")
        Pkg.add(url="https://github.com/ebjamieson97/Undid.jl")
    catch e
        Pkg.add(url="https://github.com/ebjamieson97/Undid.jl")
    end
    """)
    print("Done updating Undid.jl.")