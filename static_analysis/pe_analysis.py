def analyze_pe(file_path):
    try:
        import pefile
    except ImportError:
        return {
            "is_pe": False,
            "error": "pefile library is not installed"
        }

    try:
        pe = pefile.PE(file_path)

        sections = []
        for section in pe.sections:
            sections.append({
                "name": section.Name.rstrip(b"\x00").decode(
                    "ascii", errors="ignore"
                ),
                "virtual_size": section.Misc_VirtualSize,
                "raw_size": section.SizeOfRawData
            })

        imports = []

        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode(
                    "ascii", errors="ignore"
                )

                functions = []

                for item in entry.imports:
                    if item.name:
                        functions.append(
                            item.name.decode(
                                "ascii", errors="ignore"
                            )
                        )

                imports.append({
                    "dll": dll_name,
                    "functions": functions
                })

        return {
            "is_pe": True,
            "machine": hex(pe.FILE_HEADER.Machine),
            "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
            "sections": sections,
            "imports": imports
        }

    except Exception as error:
        return {
            "is_pe": False,
            "error": str(error)
        }
