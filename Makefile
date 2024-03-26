install:
	pipenv install

run: 
	pipenv run streamlit run app.py

plot:
	pipenv run streamlit run plot.py

test:
	echo "test"


