# Python_auto_api  
Run tests  
python -m pytest --allure_dir=test_results/ tests/ && allure serve test_result/  
or  
docker-compose up --build  
or  
docker run --rm --mount type=bind,src=full_path_to_project_folder,target=/tests/ pytest_runner  
