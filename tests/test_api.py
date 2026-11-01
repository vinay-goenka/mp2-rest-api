def test_upload_csv(client, sample_csv_bytes):
    # TODO: Upload the sample CSV to POST /upload.
    # Assert status 200, six rows, two columns,
    # and a positive integer dataset ID.
    response = client.post(
        "/upload",
        files = {
            "file": (
                "sample_data.csv",
                sample_csv_bytes,
                "text/csv"
            )
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 6
    assert data["columns"] == 2
    assert isinstance(data["id"], int)
    assert data["id"] > 0


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    process_res = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json = processing_body
    )
    assert process_res.status_code == 200
    process_data = process_res.json()
    assert process_data["validation_rows_removed"] == 1
    report = process_data["cleaning_report"]
    assert report["rows_before"] == 5
    assert report["rows_after"] == 3

    get_res = client.get(f"/datasets/{uploaded_dataset_id}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["total_rows"] == 3

    records = get_data["data"]
    student_ids = []
    scores = []
    for r in records:
        student_ids.append(r["student_id"])
        scores.append(r["score"])

    assert student_ids == [1,2,5]
    assert scores == [80, 90, 85]


def test_retrieve_missing_dataset(client):
    # TODO: Retrieve a dataset ID that does not exist.
    # Assert status 404.
    response = client.get("/datasets/999")
    assert response.status_code == 404
