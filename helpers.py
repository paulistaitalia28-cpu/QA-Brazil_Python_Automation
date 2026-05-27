{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "initial_id",
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Verifica se o Routes está ativo e funcionando. Não mude\n",
    "def is_url_reachable(url):\n",
    "    \"\"\"Verifique se a URL pode ser acessada. Passe a URL do Urban Routes como parâmetro.\n",
    "    Se puder ser alcançada, retorna True (verdadeiro), caso contrário, retorna False (falso)\"\"\"\n",
    "\n",
    "    import ssl\n",
    "    import urllib.request\n",
    "\n",
    "    try:\n",
    "        ssl_ctx = ssl.create_default_context()\n",
    "        ssl_ctx.check_hostname = False\n",
    "        ssl_ctx.verify_mode = ssl.CERT_NONE\n",
    "\n",
    "        with urllib.request.urlopen(url, context=ssl_ctx) as response:\n",
    "            # print(\"Código de status da resposta:\", response.status)# para fins de depuração\n",
    "            if response.status == 200:\n",
    "                 return True\n",
    "            else:\n",
    "                return False\n",
    "    except Exception as e:\n",
    "        print (e)\n",
    "\n",
    "    return False"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
