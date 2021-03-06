r"""
    version data.txt -------> make *class and store classes to list
    -----> check whether the classes is up to date. If not update

    *class{
        _mod_name: str
        _mod_version_from_user: str
        _mod_version_from_server: str

        func {
            class_init(){
                '''
                Set this._mod_name and this._mod_version_from_user reading text file
                Set this._mod_version_from_server requesting to server
                '''
            }

            is_latest() -> bool{
                if (this._mod_version_from_user == this._mod_version_from_server):
                    return true;
                else
                    return false;
            }
        }
    }
"""