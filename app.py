from pennapps import app

if __name__ == '__main__':
  app.debug = True
  app.run(debug=True, host='0.0.0.0', port=80)
