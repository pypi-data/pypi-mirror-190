from invenio_access.permissions import system_identity


def test_expandable_fields(sample_file_record, sample_document_record, sample_document_dict, sample_file_dict,
                           document_service):

    expected_expanded_file = {
        "metadata":
            {
                "filename": "record 1 - file 1",
                "filesize": 512
            }
    }
    #one expandable field
    doc_id = sample_document_record["id"]
    r = document_service.read(system_identity, doc_id, expand=True)
    data = r.data
    expanded = data["expanded"]["metadata"]["file"]

    assert len(data["expanded"]) == 1
    assert len(data["expanded"]["metadata"]) == 1
    assert expanded == expected_expanded_file